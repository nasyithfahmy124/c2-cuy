from django.db import models
from django.conf import settings
from petani.models import Project
# Create your models here.
class Donasi(models.Model):
    donatur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    jumlah = models.IntegerField()
    tanggal = models.DateTimeField(auto_now_add=True)