from django.urls import path
from . import views

urlpatterns = [
    path('docs/', views.pusat_edukasi, name='pusat_edukasi'),
    path('docs/<slug:slug>/', views.pusat_edukasi, name='edukasi_detail'),
]