from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .forms import FormDonasi
from django.contrib import messages
# Create your views here.
@login_required
def home_page(request):
    waktu = datetime.now()
    
    return render(request,'petani/home_p.html',{
        'waktu' : waktu
    })
    
def donasi(request):
    if request.method == 'POST':
        form = FormDonasi(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.petani = request.user
            project.save()
            return redirect('home')
    else:
        form = FormDonasi()

    return render(request, 'petani/projek.html', {'formd': form})