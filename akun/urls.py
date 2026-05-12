from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('mulai/', views.mulai_redirect, name='mulai_redirect'),
    path('beranda/', views.public_home, name='public_home'),
    path('dashboard/', views.home_page, name='dashboard'),
    path('login/', views.page_login, name='login'),
    path('register/', views.page_register, name='register'),
    path('logout/', views.logout_page, name='logout'),
    path('change-password/', views.gantipw, name='gantipw'),
    path('profile/', views.profile_user, name='profile_user'),
]