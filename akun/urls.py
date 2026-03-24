from django.urls import path
from . import views
urlpatterns = [
    path('', views.page_login,name='login'),
    path('register/',views.page_register,name='register'),
    path('logout/',views.logout_page,name='logout'),
    path('home/',views.home_page,name='home')
]
