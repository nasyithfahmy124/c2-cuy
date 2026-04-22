from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .forms import FormDonasi,FormLaporan
from django.contrib import messages
from .models import Project,Laporan
from django.db.models import Sum
from donatur.models import Donasi,DonasiBarang
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
# @login_required
# def donasi(request):
    
#     if request.method == 'POST':
#         form = FormDonasi(request.POST, request.FILES)
#         if form.is_valid():
#             project = form.save(commit=False)
#             project.petani = request.user
#             project.save()


#             messages.success(request,'Permintaan anda sedang dalam verifikasi, harap tunggu')
#             return redirect('home_p')
#     else:
#         form = FormDonasi()

#     return render(request, 'petani/projek.html', {
#         'formd': form,
        
#         })



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

    return render(request, 'petani/riwayat_donasi.html', {
        'riwayat': riwayat
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
    all = Project.objects.filter(petani=request.user).order_by("-id")
    
    return render(request, 'petani/view.html', {
        'all': all
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
def alat_masuk(request):
    barang_masuk = DonasiBarang.objects.filter(
        project__petani=request.user
    ).order_by('-id')

    return render(request, 'petani/alat_masuk.html', {
        'alat': barang_masuk
    })
