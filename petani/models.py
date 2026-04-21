from django.db import models
from django.conf import settings
from django.utils import timezone   
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
    target_dana = models.IntegerField(null=True)
    kebutuhan = models.TextField(null=True)
    estimasi_hasil = models.IntegerField(null=True)
    dana_terkumpul = models.IntegerField(default=0)
    berapa_bulan = models.CharField(max_length=200) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    @property
    def persentase(self):
        if self.target_dana and self.target_dana > 0:
            hasil = int((self.dana_terkumpul / self.target_dana) * 100)
            return min(hasil, 100) # Biar mentok di 100% kalau berlebih
        return 0
    
class Laporan(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='laporan')
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()
    jumlah_pengeluaran = models.DecimalField(max_digits=12, decimal_places=2)
    bukti = models.ImageField(upload_to='bukti_laporan/', null=True, blank=True)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul