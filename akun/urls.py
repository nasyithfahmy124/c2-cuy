from django.urls import path
from . import views
urlpatterns = [
    path('',views.home_awal,name='home_awal'),
    path('landing/', views.landing_page,name='landing'),
    path('login/', views.page_login,name='login'),
    path('register/',views.page_register,name='register'),
    path('logout/',views.logout_page,name='logout'),
    path('home/',views.home_page,name='home'),
    path('change-password/',views.gantipw,name='gantipw')
]
