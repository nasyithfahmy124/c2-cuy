from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('akun.urls')),
    path('',include('petani.urls')),
    path('',include('donatur.urls')),
    path('',include('dashboard.urls'))
]
