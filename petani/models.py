from django.db import models
from django.conf import settings
from django.utils import timezone   
from django.apps import apps
from django.db.models import Sum,F


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
    keuntungan_p = models.DecimalField(
    max_digits=12,
    decimal_places=0,
    default=0)
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
        ).aggregate(Sum('items__jumlah'))['items__jumlah__sum'] or 0

        target = self.kebutuhan_barang.aggregate(
            Sum('jumlah_dibutuhkan')
        )['jumlah_dibutuhkan__sum'] or 0

        if target == 0:
            return 0

        return round((total / target) * 100, 1)
    @property
    def total_kebutuhan_uang(self):
        return self.kebutuhan_barang.aggregate(
                total=Sum(F('harga_satuan') * F('jumlah_dibutuhkan'))
            )['total'] or 0
    

    from django.db.models import Sum, F

    @property
    def total_kebutuhan(self):
        return self.kebutuhan_barang.aggregate(
            total=Sum(F('harga_satuan') * F('jumlah_dibutuhkan'))
        )['total'] or 0


    from django.db.models import Sum, F

    @property
    def total_kebutuhan(self):
        return self.kebutuhan_barang.aggregate(
            total=Sum(F('harga_satuan') * F('jumlah_dibutuhkan'))
        )['total'] or 0


    @property
    def total_donasi_barang(self):
        from donatur.models import DonasiBarangItem

        return DonasiBarangItem.objects.filter(
            donasi__project=self
        ).aggregate(
            total=Sum(F('jumlah') * F('kebutuhan__harga_satuan'))
        )['total'] or 0


    @property
    def sisa_kebutuhan(self):
        return self.total_kebutuhan - self.total_donasi_barang


    @property
    def progress_barang(self):
        total = self.total_donasi_barang
        target = self.total_kebutuhan

        if target == 0:
            return 0

        return round((total / target) * 100, 1)
    


    @property
    def total_pengeluaran(self):
        return self.laporan.aggregate(
            total=Sum('jumlah_pengeluaran')
        )['total'] or 0

    @property
    def total_pendapatan(self):
        return self.hasil_panen.aggregate(
            total=Sum('total_pendapatan')
        )['total'] or 0

    @property
    def keuntungan_bersih(self):
        return self.total_pendapatan - self.total_pengeluaran


    @property
    def keuntungan_petani(self):
        return self.keuntungan_bersih * 0.6

    @property
    def keuntungan_donatur(self):
        return self.keuntungan_bersih * 0.4
    
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
    harga_satuan = models.IntegerField(default=0)
    satuan = models.CharField(max_length=50, default="item")  

    def __str__(self):
        return f"{self.nama_barang} ({self.project.nama})"
    @property
    def total_harga(self):
        return self.harga_satuan * self.jumlah_dibutuhkan

class HasilPanen(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='hasil_panen'
    )

    total_pendapatan = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )

    keterangan = models.TextField(
        null=True,
        blank=True
    )

    bukti_panen = models.ImageField(
        upload_to='bukti_laporan/',
        null=True,
        blank=True
    )

    tanggal_panen = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Hasil Panen - {self.project.nama}"


    