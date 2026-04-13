from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .forms import FormDonasi,FormLaporan
from django.contrib import messages
from .models import Project,Laporan
from django.db.models import Sum
from donatur.models import Donasi
# Create your views here.
@login_required
def home_page(request):
    dana_masuk = Donasi.objects.filter(
    project__petani=request.user).aggregate(total=Sum('jumlah'))['total'] or 0

    waktu = datetime.now()
    projects = Project.objects.filter(petani=request.user)
    return render(request,'petani/home_p.html',{
        'waktu' : waktu,
        'dana' : dana_masuk,
        'projects': projects 
    })
@login_required
def donasi(request):
    
    if request.method == 'POST':
        form = FormDonasi(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.petani = request.user
            project.save()
            messages.success(request,'Permintaan anda sedang dalam verifikasi, harap tunggu')
            return redirect('home_p')
    else:
        form = FormDonasi()

    return render(request, 'petani/projek.html', {
        'formd': form,
        
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
            return redirect('home_p')
    else:
        form = FormLaporan()
    
    return render(request,'petani/laporan.html',{
        'form' : form,
        'project' : project
    })

@login_required 
def view_projek(request):
    all = Project.objects.filter(petani=request.user)
    
    return render(request, 'petani/view.html', {
        'all': all
    })