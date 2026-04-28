from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.db.models.functions import Coalesce
from petani.models import Project
from donatur.models import Donasi
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import KategoriEdukasiForm,MateriEdukasiForm
from edukasi.models import MateriEdukasi,KategoriEdukasi

def admin_only(user):
    return user.is_staff  

def formlog(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard_admin')
        else:
            messages.error(request, "Login gagal atau bukan admin")

    return render(request, 'dashboard/login.html')


@login_required
@user_passes_test(admin_only)
def dashboard_admin(request):
    projects = Project.objects.filter(
        status='pending'
    ).order_by('-id')

    proyek_aktif = Project.objects.filter(
        status='aktif'
    ).annotate(
        total_donasi_db=Coalesce(Sum('donasi__jumlah'), 0)
    ).order_by('-id')
    total_dana = Donasi.objects.aggregate(Sum('jumlah'))['jumlah__sum'] or 0
    total_project = projects.count()
    total_petani = Project.objects.values('petani').distinct().count()
    return render(request, 'dashboard/home.html', {
        'projects': projects,
        'proyek_aktif': proyek_aktif,
        'total_dana': total_dana,
        'total_project': total_project,
        'total_petani': total_petani
    })


@login_required
@user_passes_test(admin_only)
def validasi_project(request, id):
    project = get_object_or_404(Project, id=id)

    project.status = 'aktif'
    project.save()

    return redirect('dashboard_admin')



@login_required
@user_passes_test(admin_only)
def tambah_kategori(request):
    form = KategoriEdukasiForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,'menambah kategori berhasil!')
        return redirect('dashboard_admin')
    return render(request, 'dashboard/kategori.html', {'form': form})

@login_required
@user_passes_test(admin_only)
def tambah_materi(request):
    form = MateriEdukasiForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,'menambah materi edukasi berhasil')
        return redirect('dashboard_admin')
    return render(request, 'dashboard/materi.html', {'form': form})
@login_required
@user_passes_test(admin_only)
def lihat_materi(request):
    materi = MateriEdukasi.objects.all()
    
    return render(request,'dashboard/materi_all.html',{
        'materi' : materi
    })
    
@login_required
@user_passes_test(admin_only)
def edit_materi(request, id):
    materi = get_object_or_404(MateriEdukasi, id=id)
    form = MateriEdukasiForm(request.POST or None, instance=materi)
    if form.is_valid():
        form.save()
        return redirect('semua_materi')
    return render(request, 'dashboard/editmateri.html', {
        'form': form,
        'title': 'Edit Materi'
    })

@login_required
@user_passes_test(admin_only)
def hapus_materi(request, id):
    materi = get_object_or_404(MateriEdukasi, id=id)
    materi.delete()
    return redirect('semua_materi')