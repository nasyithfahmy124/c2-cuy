from django.urls import path
from . import views
urlpatterns = [
    path('dashboard-petani/',views.home_page,name='home_p')
]
