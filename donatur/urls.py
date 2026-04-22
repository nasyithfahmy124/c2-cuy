from django.urls import path
from . import views
urlpatterns = [
    path('dashboard-donatur/',views.home_page,name='home_d'),
    path('danai/<int:id>/', views.danai_project, name='danai_project'),
    path('laporan/<int:id>/', views.lihat_laporan, name='lihat_laporan'),
    path('detail-project/<int:id>',views.detail,name='det'),
    path('donasi-barang/<int:id>/', views.donasi_barang, name='donasi_barang'),
]
