from django.db import models
from django.conf import settings

STATUS_CHOICES = [
    ('pending', 'Menunggu'),
    ('aktif', 'Sedang Didanai'),
    ('selesai', 'Selesai'),
]


class Project(models.Model):
    petani = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    target_dana = models.IntegerField()
    dana_terkumpul = models.IntegerField(default=0)
    foto_lahan = models.ImageField(upload_to='lahan/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    kebutuhan = models.TextField()