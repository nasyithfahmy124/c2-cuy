from django.db import models
from django.conf import settings
from petani.models import Project
# Create your models here.
class Donasi(models.Model):
    donatur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    tanggal = models.DateTimeField(auto_now_add=True)
    keuntungan_d = models.DecimalField(max_digits=12,decimal_places=0,default=0)
    dana_terkumpul = models.DecimalField(
    max_digits=12,
    decimal_places=0,
    default=0
)

class DonasiBarang(models.Model):
    STATUS_CHOICES = [
        ('diajukan', 'Diajukan'),
        ('disetujui', 'Disetujui'),
        ('ditolak', 'Ditolak'),
        ('dikirim', 'Dikirim'),
    ]

    donatur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    kebutuhan = models.ForeignKey(
        'petani.KebutuhanBarang',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    
    nama_barang_custom = models.CharField(max_length=100, null=True, blank=True)

    jumlah = models.IntegerField()
    deskripsi = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='diajukan')
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nama_barang_custom or (self.kebutuhan.nama_barang if self.kebutuhan else "Barang")