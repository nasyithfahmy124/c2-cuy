from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import Coalesce
from petani.models import Project
from .forms import *

def landing_page(request):
    # Halaman default (halaman awal)
    return render(request, 'landing.html')

def mulai_redirect(request):
    if request.user.is_authenticated:
        user = request.user

        if user.role == 'petani':
            return redirect('home_p')
        elif user.role == 'donatur':
            return redirect('home_d')
        else:
            return redirect('public_home')  # fallback

    else:
        return redirect('public_home')
    
def public_home(request):
    projects = Project.objects.filter(status='aktif').annotate(
        total_donasi_db=Coalesce(Sum('donasi__jumlah'), 0)
    ).order_by('-id')

    return render(request, 'login/home_page.html', {
        'projects': projects
    })

@login_required
def home_page(request):
    user = request.user

    if user.role == 'petani':
        return redirect('home_p')
    elif user.role == 'donatur':
        return redirect('home_d')
    else:
        return redirect('public_home')

@login_required
def profile_user(request):
    return render(request, 'login/profile_user.html', {
        'user_login': request.user
    })

def page_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                if user.role == 'petani':
                    return redirect('home_p')
                elif user.role == 'donatur':
                    return redirect('home_d')
            else:
                messages.error(request, 'Username atau password salah')

    return render(request, 'login/login.html', {
        'form': form
    })

    


def page_register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form_register = RegisterForm(request.POST)
        if form_register.is_valid():
            form_register.save()
            messages.success(request, 'Akun berhasil dibuat. Silakan masuk.')
            return redirect('login')
    else:
        form_register = RegisterForm()

    return render(request, 'login/register.html', {
        'form': form_register
    })
    
def logout_page(request):
    logout(request) 
    return redirect('landing')

@login_required
def gantipw(request):
    form = GantiPwForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Ubah password berhasil!')
        return redirect('dashboard')
    else:
        form = GantiPwForm(request.user)
        
    return render(request, 'login/gantipw.html', {
        'form': form
    })