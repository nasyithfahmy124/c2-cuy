from django.db import models
from django.conf import settings
from django.utils import timezone   
from django.apps import apps
from django.db.models import Sum


STATUS_CHOICES = [
    ('pending', 'Menunggu'),
    ('aktif', 'Sedang Didanai'),
    ('selesai', 'Selesai'),
]


class Project(models.Model):
    petani = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(null=True)
    lokasi = models.CharField(max_length=200, null=True)
    luas_lahan = models.IntegerField(null=True)
    foto_lahan = models.ImageField(upload_to='lahan/', null=True)
    target_dana = models.DecimalField(max_digits=12, decimal_places=0, default=0)    
    kebutuhan = models.TextField(null=True)
    estimasi_hasil = models.IntegerField(null=True)
    berapa_bulan = models.CharField(max_length=200) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    no_hp = models.CharField(max_length=15) 
    
    @property
    def total_donasi(self):
        Donasi = apps.get_model('donatur', 'Donasi')

        return Donasi.objects.filter(
            project=self
        ).aggregate(Sum('jumlah'))['jumlah__sum'] or 0


    @property
    def persentase(self):
        total = self.total_donasi

        if self.target_dana:
            return round((total / self.target_dana) * 100, 1)

        return 0


    @property
    def progress_barang(self):
        DonasiBarang = apps.get_model('donatur', 'DonasiBarang')

        total = DonasiBarang.objects.filter(
            project=self,
            status='disetujui'
        ).aggregate(Sum('jumlah'))['jumlah__sum'] or 0

        target = self.kebutuhan_barang.aggregate(
            Sum('jumlah_dibutuhkan')
        )['jumlah_dibutuhkan__sum'] or 0

        if target == 0:
            return 0

        return round((total / target) * 100, 1)

    
    
        
class Laporan(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='laporan')
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()
    jumlah_pengeluaran = models.DecimalField(max_digits=12, decimal_places=2)
    bukti = models.ImageField(upload_to='bukti_laporan/', null=True, blank=True)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul

class KebutuhanBarang(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='kebutuhan_barang')
    
    nama_barang = models.CharField(max_length=100)
    jumlah_dibutuhkan = models.IntegerField()

    def __str__(self):
        return f"{self.nama_barang} ({self.project.nama})"

