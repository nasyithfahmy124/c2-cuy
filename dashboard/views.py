from django.shortcuts import render, get_object_or_404, redirect
from petani.models import Project

def validasi_project(request, id):
    project = get_object_or_404(Project, id=id)
    
    project.status = 'aktif'
    project.save()
    
    return redirect('dashboard_admin')

def dashboard_admin(request):
    projects = Project.objects.filter(status='pending')
    
    return render(request, 'dashboard/home.html', {
        'projects': projects
    })

def home_awal(request):
    proyek_aktif = Project.objects.filter(status='aktif').annotate(
        total_donasi=Coalesce(Sum('donasi__jumlah'), 0)
    ).order_by('-id') #

    return render(request, '')