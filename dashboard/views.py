from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.db.models.functions import Coalesce
from petani.models import Project
from donatur.models import Donasi
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

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

