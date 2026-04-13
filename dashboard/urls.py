from django.urls import path
from . import views

urlpatterns = [
    # path('', views.login_admin, name='login_admin'),  # /adminuser/
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('validasi/<int:id>/', views.validasi_project, name='validasi_project'),
]