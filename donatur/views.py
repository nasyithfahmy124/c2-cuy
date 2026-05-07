from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import FormDonasi,FormDonasiBarang
from petani.models import Project,Laporan,KebutuhanBarang
from .forms import FormDonasiBarang,FormDonasiBarangItem,DonasiBarangItemFormSet
from django.db.models import Sum, Value,F
from .models import Donasi,DonasiBarang,DonasiBarangItem
from django.contrib import messages
from itertools import chain
from django.db.models.functions import Coalesce
from django.forms import inlineformset_factory
from django.db.models import Q
# Create your views here.
@login_required
def home_page(request):
    projects = Project.objects.filter(status='aktif').annotate(
        total_donasi_db=Sum('donasi__jumlah')
    ).order_by('-id')

    projects = Project.objects.filter(status='aktif').annotate(
    total_donasi_db=Coalesce(Sum('donasi__jumlah'), Value(0))
)

    total_dana = Donasi.objects.aggregate(Sum('jumlah'))['jumlah__sum'] or 0
    total_project = projects.count()
    total_petani = Project.objects.values('petani').distinct().count()
    
    #donasiuser
    total = Donasi.objects.filter(donatur=request.user).aggregate(
    total_jumlah=Sum('jumlah')
)

    return render(request, 'donatur/home_d.html', {
        'projects': projects,
        'total_dana': total_dana,
        'total_project': total_project,
        'total_petani': total_petani,
        'total_uang' : total['total_jumlah'] or 0
    })

@login_required
def danai_project(request, id):
    project = get_object_or_404(Project, id=id)

    if project.status != 'aktif':
        return redirect('home_d')

    if request.method == 'POST':
        form = FormDonasi(request.POST)
        if form.is_valid():
            jumlah = form.cleaned_data['jumlah']

            # hitung total REAL dari database
            total = Donasi.objects.filter(project=project).aggregate(
                Sum('jumlah')
            )['jumlah__sum'] or 0

            sisa = project.target_dana - total

            if jumlah > sisa:
                form.add_error('jumlah', f'Maksimal donasi: {sisa}')
            else:
                funding = form.save(commit=False)
                funding.donatur = request.user
                funding.project = project
                funding.save()

                # cek status
                total_baru = total + jumlah
                if total_baru >= project.target_dana:
                    project.status = 'selesai'
                else:
                    project.status = 'aktif'

                project.save()
                messages.success(request,'Bantuan berhasil dikirim, terima kasih atas partisipasi anda!')
                return redirect('home_d')
    else:
        form = FormDonasi()

    return render(request, 'donatur/donasi.html', {
        'form': form,
        'project': project
    })
    

def donasi_barang(request, id):
    project = Project.objects.get(id=id)

    DonasiBarangItemFormSet = inlineformset_factory(
        DonasiBarang,
        DonasiBarangItem,
        form=FormDonasiBarangItem,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        form = FormDonasiBarang(request.POST)
        formset = DonasiBarangItemFormSet(
                    request.POST,
                    form_kwargs={'project': project}
                )
        # 🔥 inject project ke setiap form
        # for f in formset.forms:
        #     f.fields['kebutuhan'].queryset = KebutuhanBarang.objects.filter(project=project)

        if form.is_valid() and formset.is_valid():
            donasi = form.save(commit=False)
            donasi.donatur = request.user
            donasi.project = project
            donasi.save()

            formset.instance = donasi
            formset.save()

            return redirect('home_d')

    else:
        form = FormDonasiBarang()

        formset = DonasiBarangItemFormSet(
            form_kwargs={'project': project}
        )

    return render(request, 'donatur/danaibarang.html', {
        'form': form,
        'formset': formset,
    })

@login_required
def lihat_laporan(request, id):
    project = get_object_or_404(Project, id=id)
    laporan = project.laporan.all().order_by('-tanggal')

    return render(request, 'donatur/laporan_fp.html', {
        'project': project,
        'laporan': laporan
    })
    
@login_required
def detail(request, id):
    det = get_object_or_404(Project, id=id)

    total = Donasi.objects.filter(project=det).aggregate(
        Sum('jumlah')
    )['jumlah__sum'] or 0

    return render(request, 'donatur/detail.html', {
        'detail': det,
        'total_donasi_db': total
    })
@login_required 
def detail_donasi(request):
    riwayat = Donasi.objects.filter(donatur=request.user)
    riwayat_barang = DonasiBarang.objects.filter(donatur=request.user).prefetch_related('items')
    for r in riwayat:
        r.tipe = 'uang'

    for b in riwayat_barang:
        b.tipe = 'barang'

    semua_riwayat = sorted(
        chain(riwayat, riwayat_barang),
        key=lambda x: x.tanggal,
        reverse=True
    )
    print("RIWAYAT BARANG:", riwayat_barang)

    return render(request,'donatur/riwayat.html',{
        'semua': semua_riwayat,

    })
@login_required
def laporan_donatur(request):
    project_ids = Donasi.objects.filter(
        donatur=request.user).values_list('project_id', flat=True)
    laporan = Laporan.objects.filter(
        project_id__in=project_ids
    ).order_by('-tanggal')

    return render(request, 'donatur/laporan_donatur.html', {
        'laporan': laporan
    })
    
from django.db.models import Sum

from django.db.models import Sum, F
@login_required
def bagihasil(request):

    # total bantuan uang
    uang = Donasi.objects.filter(
        donatur=request.user
    ).aggregate(
        total=Sum('jumlah')
    )['total'] or 0

    # total bantuan barang (nilai rupiah)
    total_barang = DonasiBarangItem.objects.filter(
        donasi__donatur=request.user
    ).aggregate(
        total=Sum(
            F('jumlah') * F('kebutuhan__harga_satuan')
        )
    )['total'] or 0

    # total saldo bantuan
    total_saldo = uang + total_barang

    # petani dari donasi uang
    petani_uang = Donasi.objects.filter(
        donatur=request.user
    ).values_list(
        'project__petani_id',
        flat=True
    )

    # petani dari donasi barang
    petani_barang = DonasiBarang.objects.filter(
        donatur=request.user
    ).values_list(
        'project__petani_id',
        flat=True
    )

    jumlah_petani = len(
        set(list(petani_uang) + list(petani_barang))
    )
    return render(request, 'donatur/bagihasil.html', {
        'total_uang': uang,
        'bantuan_u': uang,
        'nilai_barang': total_barang,
        'uang_barang': total_saldo,
        'jumlah_petani': jumlah_petani,
        
    })
    
@login_required
def yangdibantu(request):
    projects = Project.objects.filter(
        Q(donasi__donatur=request.user) |
        Q(donasibarang__donatur=request.user)
    ).distinct()
    
    return render(request,'donatur/yangdidanai.html',{
        'projects': projects,
    })
@login_required
def laporan2(request, id):

    project = get_object_or_404(
        Project.objects.filter(
            Q(donasi__donatur=request.user) |
            Q(donasibarang__donatur=request.user)
        ).distinct(),
        id=id
    )

    laporan = project.laporan.all()
    hasil_panen = project.hasil_panen.all()

    return render(request, 'donatur/laporan_bantuan.html', {
        'project': project,
        'laporan': laporan,
        'hasil_panen': hasil_panen,
    })