from django.db import models
from django.utils.text import slugify

class KategoriEdukasi(models.Model):
    nama = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, help_text="Class icon Phosphor, contoh: ph-plant", null=True, blank=True)
    urutan = models.IntegerField(default=0, help_text="Urutan tampil di halaman edukasi")

    class Meta:
        verbose_name_plural = "Kategori Edukasi"
        ordering = ['urutan']

    def __str__(self):
        return self.nama

class MateriEdukasi(models.Model):
    ROLE_TARGET = [
        ('semua', 'Umum (Petani & Investor)'),
        ('petani', 'Khusus Petani Milenial'),
        ('donatur', 'Khusus Investor'),
    ]  

    kategori = models.ForeignKey(KategoriEdukasi, on_delete=models.CASCADE, related_name='materi')
    judul = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    konten = models.TextField(help_text="Format HTML/Text untuk isi materi")
    target_role = models.CharField(max_length=20, choices=ROLE_TARGET, default='semua')
    waktu_baca = models.IntegerField(default=5, help_text="Estimasi waktu baca (menit)")
    urutan = models.IntegerField(default=0, help_text="Urutan materi di dalam kategori")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Materi Edukasi"
        ordering = ['kategori', 'urutan']

    from django.utils.text import slugify

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.judul)
            slug = base_slug
            counter = 1

            while MateriEdukasi.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.kategori.nama} - {self.judul}"