from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .forms import FormDonasi
from django.contrib import messages
from .models import Project
from django.db.models import Sum
from donatur.models import Donasi
# Create your views here.
@login_required
def home_page(request):
    dana_masuk = Donasi.objects.filter(
    project__petani=request.user).aggregate(total=Sum('jumlah'))['total'] or 0

    waktu = datetime.now()
    
    return render(request,'petani/home_p.html',{
        'waktu' : waktu,
        'dana' : dana_masuk
    })
    
def donasi(request):
    
    if request.method == 'POST':
        form = FormDonasi(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.petani = request.user
            project.save()
            return redirect('home_p')
    else:
        form = FormDonasi()

    return render(request, 'petani/projek.html', {
        'formd': form,
        
        })