from django.urls import path
from . import views
urlpatterns = [
    path('donatur/dashboard-donatur/',views.home_page,name='home_d'),
    path('donatur/danai/<int:id>/', views.danai_project, name='danai_project'),
    path('donatur/laporan/<int:id>/', views.lihat_laporan, name='lihat_laporan'),
    path('donatur/detail-project/<int:id>',views.detail,name='det'),
    path('donatur/donasi-barang/<int:id>/', views.donasi_barang, name='donasi_barang'),
    path('riwayat-donatur/',views.detail_donasi,name='riwayat_d'),
    path('laporan-donatur/', views.laporan_donatur, name='laporan_donatur')
]
