from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('dashboard-petani/',views.home_page,name='home_p'),
    path('buat-projek-petani/',views.donasi,name='projek'),
    path('laporan/tambah/<int:project_id>/', views.laporan, name='tambah_laporan'),
    path('semua-projek/',views.view_projek,name='allp'),
    path('detail/<int:id>/',views.detail_projek,name='detail'),
]

static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)