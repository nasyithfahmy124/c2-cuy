from django.urls import path
from . import views
urlpatterns = [
    path('dashboard-donatur/',views.home_page,name='home_d'),
    path('danai/<int:id>/', views.danai_project, name='danai_project'),
]
