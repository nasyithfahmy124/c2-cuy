from collections import defaultdict
from decimal import Decimal
from datetime import datetime
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum, Q, F
from django.shortcuts import render, redirect, get_object_or_404

from .forms import (
    FormDonasi,
    FormLaporan,
    formhasilpanen,
)

from .models import (
    Project,
    Laporan,
    HasilPanen,
    KebutuhanBarang,
)

from donatur.models import (
    Donasi,
    DonasiBarang,
    DonasiBarangItem,
)
# Create your views here.
@login_required
def home_page(request):
    dana_masuk = Donasi.objects.filter(
    project__petani=request.user).aggregate(total=Sum('jumlah'))['total'] or 0
    total_alat = DonasiBarang.objects.filter(
    project__petani=request.user
    ).aggregate(total=Sum('items__jumlah'))['total'] or 0
    total_barang = DonasiBarangItem.objects.filter(
        donasi__project__petani=request.user
    ).aggregate(
        total=Sum(F('jumlah') * F('kebutuhan__harga_satuan'))
    )['total'] or 0

    # 🔥 TOTAL SEMUA
    total_bantuan = dana_masuk + total_barang
    waktu = datetime.now()
    projects = Project.objects.filter(petani=request.user).order_by("-id")
    print("TOTAL BARANG:", total_barang)
    return render(request,'petani/home_p.html',{
        'waktu' : waktu,
        'dana' : dana_masuk,
        'projects': projects,
        'alat' : total_alat ,
        'totalbantuan' : total_bantuan,
        'nilaibarang' : total_barang
    })

@login_required
def donasi(request):

    if request.method == 'POST':

        form = FormDonasi(request.POST, request.FILES)

        if form.is_valid():

            try:
                with transaction.atomic():

                    project = form.save(commit=False)
                    project.petani = request.user
                    project.save()

                    nama_barang_list = request.POST.getlist('nama_barang[]')
                    jumlah_barang_list = request.POST.getlist('jumlah_barang[]')
                    harga_list = request.POST.getlist('harga_satuan[]')
                    satuan_list = request.POST.getlist('satuan[]')

                    for nama, jumlah, harga, satuan in zip(
                        nama_barang_list,
                        jumlah_barang_list,
                        harga_list,
                        satuan_list
                    ):

                        if nama and jumlah:

                            try:
                                jumlah = int(jumlah)
                                harga = int(harga) if harga else 0

                            except ValueError:
                                continue

                            KebutuhanBarang.objects.create(
                                project=project,
                                nama_barang=nama,
                                jumlah_dibutuhkan=jumlah,
                                harga_satuan=harga,
                                satuan=satuan or "item"
                            )

                messages.success(
                    request,
                    'Project dan kebutuhan berhasil dibuat!'
                )

                return redirect('home_p')

            except Exception as e:

                messages.error(
                    request,
                    f'Terjadi error: {e}'
                )

        else:

            print(form.errors)

            messages.error(
                request,
                'Form gagal dikirim. Periksa kembali input Anda.'
            )

    else:

        form = FormDonasi()

    return render(request, 'petani/projek.html', {
        'formd': form,
    })

@login_required
def riwayat_donasi(request):
    riwayat = Donasi.objects.filter(
        project__petani=request.user
    ).select_related('donatur', 'project').order_by('-tanggal')


    total = riwayat.aggregate(total=Sum('jumlah'))['total'] or 0
    count = riwayat.count()
    return render(request, 'petani/riwayat_donasi.html', {
        'riwayat': riwayat,
        'total_donasi': total,
        'jumlah_donasi': count
    })

@login_required
def laporan(request, project_id):
    project = get_object_or_404(Project, id=project_id, petani=request.user)

    if request.method == 'POST':
        form = FormLaporan(request.POST,request.FILES)
        if form.is_valid():
            laporan = form.save(commit=False)
            laporan.project = project
            laporan.save()
            messages.success(request,"Laporan berhasil dikirim ke donatur!")
            return redirect('home_p')
    else:
        form = FormLaporan()
    
    return render(request,'petani/laporan.html',{
        'form' : form,
        'project' : project
    })

@login_required 
def view_projek(request):
    search_query = request.GET.get('q', '')
    current_status = request.GET.get('status', 'semua')
    all_projects = Project.objects.filter(petani=request.user).order_by("-id")

    if search_query:
        all_projects = all_projects.filter(
            Q(nama__icontains=search_query) | Q(lokasi__icontains=search_query)
        )
    
    if current_status == 'aktif':
        all_projects = all_projects.filter(status='Aktif') 
    elif current_status == 'selesai':
        all_projects = all_projects.filter(status='Selesai')

    return render(request, 'petani/view.html', {
        'all': all_projects, 
        'search_query': search_query,
        'current_status': current_status
    })

def detail_projek(request, id):

    project = get_object_or_404(
        Project.objects.select_related('petani'),
        id=id,
        petani=request.user
    )

    barang_masuk = (
        DonasiBarang.objects
        .filter(project=project)
        .prefetch_related('items')
        .order_by('-id')
    )

    total_donasi = (
        project.donasi_set.aggregate(
            total=Coalesce(Sum('jumlah'), 0)
        )['total']
    )

    return render(request, 'petani/detail_projek.html', {
        'semua_projek': project,
        'total_donasi': total_donasi,
        'barang_masuk': barang_masuk,
    })

@login_required
def hapus_project(request,id):
    hps = get_object_or_404(Project,id=id,petani = request.user)
    if request.method == "POST" :
        hps.delete()
        messages.success(request,"Hapus project berhasil bos")
        return redirect('home_p')





@login_required
def alat_masuk(request):
    items = DonasiBarangItem.objects.filter(
        donasi__project__petani=request.user
    )

    kebutuhan = KebutuhanBarang.objects.filter(
        project__petani=request.user
    )

    data = defaultdict(lambda: {"masuk": 0, "target": 0})
    for k in kebutuhan:
        data[k.nama_barang]["target"] += k.jumlah_dibutuhkan * k.harga_satuan
    for item in items:
        nama = item.kebutuhan.nama_barang
        data[nama]["masuk"] += item.jumlah * item.kebutuhan.harga_satuan

    tracking = []
    total_masuk = 0
    total_target = 0

    for nama, val in data.items():
        masuk = val["masuk"]
        target = val["target"] or 1

        persen = round((masuk / target) * 100, 1)

        tracking.append({
            "nama": nama,
            "masuk": masuk,
            "target": target,
            "persen": persen
        })

        total_masuk += masuk
        total_target += target

    progress_total = round((total_masuk / total_target) * 100, 1) if total_target else 0
    
    return render(request, 'petani/alat_masuk.html', {
        'tracking': tracking,
        'total_uang_masuk': total_masuk,
        'total_kebutuhan_uang': total_target,
        'sisa_uang': total_target - total_masuk,
        'progress_total': progress_total,
    })
from django.db.models import Sum, F
from decimal import Decimal
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def bagihasil(request):

    dana_masuk = Donasi.objects.filter(
        project__petani=request.user
    ).aggregate(total=Sum('jumlah'))['total'] or 0

    total_alat = DonasiBarang.objects.filter(
        project__petani=request.user
    ).aggregate(total=Sum('items__jumlah'))['total'] or 0

    total_barang = DonasiBarangItem.objects.filter(
        donasi__project__petani=request.user
    ).aggregate(
        total=Sum(F('jumlah') * F('kebutuhan__harga_satuan'))
    )['total'] or 0

    total_bantuan = dana_masuk + total_barang
    total_pengeluaran = Laporan.objects.filter(
        project__petani=request.user
    ).aggregate(
        total=Sum('jumlah_pengeluaran')
    )['total'] or 0

    total_pendapatan = HasilPanen.objects.filter(
        project__petani=request.user
    ).aggregate(
        total=Sum('total_pendapatan')
    )['total'] or 0

    keuntungan_bersih = total_pendapatan - total_pengeluaran

    keuntungan_petani = keuntungan_bersih * Decimal('0.6')
    keuntungan_donatur = keuntungan_bersih * Decimal('0.4')

    projects = Project.objects.filter(
        petani=request.user
    ).order_by("-id")

    return render(request, 'petani/bagihasil.html', {
        'waktu': now(),
        'dana': dana_masuk,
        'projects': projects,
        'alat': total_alat,
        'totalbantuan': total_bantuan,
        'nilaibarang': total_barang,
    
        'total_pengeluaran': total_pengeluaran,
        'total_pendapatan': total_pendapatan,
        'keuntungan_bersih': keuntungan_bersih,
        'keuntungan_petani': keuntungan_petani,
        'keuntungan_donatur': keuntungan_donatur,
    })
    
@login_required
def laporan_panen_bagihasil(request,project_id):
    project = get_object_or_404(
        Project,
        id=project_id,
        petani=request.user
    )

    if request.method == "POST":
        form = formhasilpanen(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            hasil_panen = form.save(commit=False)

            hasil_panen.project = project

            hasil_panen.save()

            messages.success(
                request,
                "Hasil panen berhasil ditambahkan!"
            )

            return redirect('bagihasil_p')

    else:
        form = formhasilpanen()
    
    context = {
        'project': project,
        'form': form
    }

    return render(
        request,
        'petani/hasil_panen.html',
        context
    )