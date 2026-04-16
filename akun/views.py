from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *

# ==========================================
# 1. HALAMAN UTAMA & REDIRECTOR
# ==========================================

def landing_page(request):
    # Halaman default (halaman awal)
    return render(request, 'landing.html')

def mulai_redirect(request):
    # Logika ketika tombol "Mulai" di-klik
    if request.user.is_authenticated:
        # Jika sudah login, arahkan ke dashboard
        return redirect('dashboard')
    else:
        # Jika belum login, arahkan ke halaman home biasa
        return redirect('public_home')

def public_home(request):
    # Merender halaman templates/home.html (Untuk tamu/belum login)
    return render(request, 'home.html')

@login_required
def home_page(request):
    # Merender halaman dasbor (Untuk user yang sudah login)
    # Sesuaikan path template-nya sesuai struktur foldermu
    return render(request, 'login/home_page.html')


# ==========================================
# 2. AUTENTIKASI (LOGIN, REGISTER, LOGOUT)
# ==========================================

def page_login(request):
    # Cegah user yang sudah login buka halaman login lagi
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Sesuai request, semua user yang login diarahkan ke dashboard
                return redirect('dashboard')
            else:
                messages.error(request, 'Username atau password salah')

    return render(request, 'login/login.html', {
        'form': form
    })

def page_register(request):
    # Cegah user yang sudah login buka halaman register
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form_register = RegisterForm(request.POST)
        if form_register.is_valid():
            form_register.save()
            messages.success(request, 'Akun berhasil dibuat. Silakan masuk.')
            # Setelah register, arahkan ke login
            return redirect('login')
    else:
        form_register = RegisterForm()

    return render(request, 'login/register.html', {
        'form': form_register
    })
    
def logout_page(request):
    logout(request) 
    # Setelah logout, kembalikan ke landing page
    return redirect('landing')


# ==========================================
# 3. PENGATURAN AKUN
# ==========================================

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