from django.urls import path
from . import views

urlpatterns = [
    # Halaman Default (Landing)
    path('', views.landing_page, name='landing'),
    
    # URL Perantara untuk Tombol Mulai
    path('mulai/', views.mulai_redirect, name='mulai_redirect'),
    
    # Halaman untuk User BELUM Login (templates/home.html)
    path('beranda/', views.public_home, name='public_home'),
    
    # Halaman untuk User SUDAH Login (akun/templates/home_page.html)
    path('dashboard/', views.home_page, name='dashboard'),
    
    # Autentikasi
    path('login/', views.page_login, name='login'),
    path('register/', views.page_register, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('change-password/', views.gantipw, name='gantipw')
]