from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import Register,GantiPwForm

# Create your views here.
def home_awal(request):
    
    return render(request,'home.html')

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,'landing.html')

def page_login(request):
    if request.method == "POST":
        usn = request.POST.get('username')
        pw = request.POST.get('password')
        user = authenticate(request,username = usn,password = pw)
        if user is not None:
            login(request,user)
            messages.success(request,'Login berhasil')
            return redirect('home')
        else:
            messages.error(request,'Login gagal!')
            return redirect('login')
    return render(request,'login/login.html')

def page_register(request):
    if request.method == "POST":
        form_register = Register(request.POST)
        if form_register.is_valid():
            form_register.save()
            messages.success(request,'Akun berhasil dibuat')
            return redirect('home')
    else:
        form_register = Register()
        
    
    return render(request,'login/register.html',{
        'form' : form_register
    })
    
def logout_page(request):
    logout(request) 
    messages.success(request,'bisa logout cuyy')
    return redirect('login')

    
    
@login_required
def home_page(request):
    
    return render(request,'login/home_page.html')

@login_required
def gantipw(request):
    form = GantiPwForm(request.user,request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,'Ubah password berhasil!')
        return redirect('home')
    else:
        form = GantiPwForm(request.user)
    return render(request,'login/gantipw.html',{
        'form' : form
    })

    
