from django.urls import path
from . import views

urlpatterns = [
    path('edukasi-petani/', views.pusat_edukasi, name='pusat_edukasi'),
    path('edukasi-petani/<slug:slug>/', views.pusat_edukasi, name='edukasi_detail'),
]