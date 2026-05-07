from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('petani/dashboard-petani/', views.home_page, name='home_p'),
    path('petani/buat-projek-petani/', views.donasi, name='projek'),
    path('petani/laporan/tambah/<int:project_id>/', views.laporan, name='tambah_laporan'),
    path('petani/semua-projek/', views.view_projek, name='allp'),
    path('petani/detail/<int:id>/', views.detail_projek, name='detail'),
    path('petani/<int:id>/hapus-project/', views.hapus_project, name="delete"),
    path('petani/petani/alat-masuk/', views.alat_masuk, name='alat_in'),
    path('petani/riwayat-donasi/', views.riwayat_donasi, name='riwayat_donasi'),
    path('petani/bagi-hasil',views.bagihasil,name='bagihasil_p'),
    path('petani/hasil-panen/<int:project_id>/',views.laporan_panen_bagihasil,name='laporan_panen')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)