from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('dashboard-petani/',views.home_page,name='home_p'),
    path('buat-projek-petani/',views.donasi,name='projek')
]

static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)