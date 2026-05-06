from django.db import models
from django.conf import settings
from petani.models import Project
from django.core.exceptions import ValidationError

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
    project = models.ForeignKey('petani.Project', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='diajukan')
    tanggal = models.DateTimeField(auto_now_add=True)

    def total_harga(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        return f"Donasi {self.id} - {self.project.nama}"

class DonasiBarangItem(models.Model):
    donasi = models.ForeignKey(DonasiBarang, related_name='items', on_delete=models.CASCADE)
    kebutuhan = models.ForeignKey('petani.KebutuhanBarang', on_delete=models.CASCADE)
    jumlah = models.IntegerField()

    def subtotal(self):
        return self.jumlah * self.kebutuhan.harga_satuan

    def __str__(self):
        return f"{self.kebutuhan.nama_barang} x {self.jumlah}"
    
    def clean(self):
    

        total_sudah = DonasiBarangItem.objects.filter(
            kebutuhan=self.kebutuhan
        ).exclude(id=self.id).aggregate(
            total=Sum('jumlah')
        )['total'] or 0

        total_baru = total_sudah + self.jumlah

        if total_baru > self.kebutuhan.jumlah_dibutuhkan:
            raise ValidationError(
                f"Melebihi kebutuhan! Maksimal sisa: {self.kebutuhan.jumlah_dibutuhkan - total_sudah}"
            )
    
# class KeuntunganDonatur(models.Model):
#     untung_d  = models.DecimalField(max_digits=12,decimal_places=0,default=0)