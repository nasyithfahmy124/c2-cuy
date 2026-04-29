from collections import defaultdict
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .forms import FormDonasi, FormLaporan
from django.contrib import messages
from .models import KebutuhanBarang, Project,Laporan  
from django.db.models import Sum, Q
from donatur.models import Donasi,DonasiBarang
import json

# Create your views here.
@login_required
def home_page(request):
    dana_masuk = Donasi.objects.filter(
    project__petani=request.user).aggregate(total=Sum('jumlah'))['total'] or 0
    total_alat = DonasiBarang.objects.filter(
        project__petani=request.user
    ).aggregate(total=Sum('jumlah'))['total'] or 0

    waktu = datetime.now()
    projects = Project.objects.filter(petani=request.user).order_by("-id")
    return render(request,'petani/home_p.html',{
        'waktu' : waktu,
        'dana' : dana_masuk,
        'projects': projects,
        'alat' : total_alat 
    })

@login_required
def donasi(request):
    if request.method == 'POST':
        form = FormDonasi(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.petani = request.user
            project.save()

            nama_barang_list = request.POST.getlist('nama_barang[]')
            jumlah_barang_list = request.POST.getlist('jumlah_barang[]')

            for nama, jumlah in zip(nama_barang_list, jumlah_barang_list):
                if nama and jumlah:
                    KebutuhanBarang.objects.create(
                        project=project,
                        nama_barang=nama,
                        jumlah_dibutuhkan=jumlah
                    )

            messages.success(request, 'Project dan kebutuhan berhasil dibuat!')
            return redirect('home_p')
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

@login_required
def detail_projek(request, id):
    get = get_object_or_404(
        Project,
        id=id,
        petani=request.user 
    )
    barang_masuk = DonasiBarang.objects.filter(project=get).order_by('-id')
    total = get.donasi_set.aggregate(Sum('jumlah'))['jumlah__sum'] or 0

    return render(request, 'petani/detail_projek.html', {
        'semua_projek': get,
        'total_donasi': total,
        'barang_masuk': barang_masuk
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
    barang_masuk = DonasiBarang.objects.filter(
        project__petani=request.user
    )

    kebutuhan = KebutuhanBarang.objects.filter(
        project__petani=request.user
    )

    data = defaultdict(lambda: {"masuk": 0, "target": 0})

    for k in kebutuhan:
        data[k.nama_barang]["target"] += k.jumlah_dibutuhkan

    for b in barang_masuk:
        nama = b.nama_barang_custom or (b.kebutuhan.nama_barang if b.kebutuhan else "Lainnya")
        data[nama]["masuk"] += b.jumlah

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

    labels = [item["nama"] for item in tracking]
    data_masuk = [item["masuk"] for item in tracking]
    data_target = [item["target"] for item in tracking]

    progress_total = round((total_masuk / total_target) * 100, 1) if total_target else 0

    return render(request, 'petani/alat_masuk.html', {
        'alat': barang_masuk.order_by('-id'),
        'tracking': tracking,
        'total_barang': total_masuk,
        'total_kebutuhan': total_target,
        'progress_total': progress_total,
        'labels': json.dumps(labels),
        'data_masuk': json.dumps(data_masuk),
        'data_target': json.dumps(data_target),
    })
