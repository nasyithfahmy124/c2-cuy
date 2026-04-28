from django.urls import path
from . import views

urlpatterns = [
    # path('', views.login_admin, name='login_admin'),  # /adminuser/
    path('admin-login/', views.formlog, name='login_admin'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('validasi/<int:id>/', views.validasi_project, name='validasi_project'),
    path('tambah-kategori/',views.tambah_kategori,name='kategori'),
    path('tambah-materi/',views.tambah_materi,name='materi'),
    path('semua-materi/',views.lihat_materi,name='semua_materi'),
    path('materi/edit/<int:id>/', views.edit_materi, name='materi_edit'),
    path('materi/hapus/<int:id>/', views.hapus_materi, name='materi_hapus'),
]