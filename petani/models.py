from django.db import models
from django.conf import settings

STATUS_CHOICES = [
    ('pending', 'Menunggu'),
    ('aktif', 'Sedang Didanai'),
    ('selesai', 'Selesai'),
]


class Project(models.Model):
    petani = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # dasar
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(null=True)

    # validasi
    lokasi = models.CharField(max_length=200, null=True)
    luas_lahan = models.IntegerField(null=True)
    foto_lahan = models.ImageField(upload_to='lahan/', null=True)

    # dana
    target_dana = models.IntegerField(null=True)
    kebutuhan = models.TextField(null=True)
    estimasi_hasil = models.IntegerField(null=True)

    # waktu
    tanggal_mulai = models.DateField(null=True)
    estimasi_panen = models.DateField(null=True)
    # status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
