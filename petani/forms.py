from django import forms
from .models import *

class FormDonasi(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['petani','estimasi_hasil','dana_terkumpul','status','luas_lahan',]
class FormLaporan(forms.ModelForm):
    class Meta:
        model = Laporan
        fields = ['judul', 'deskripsi', 'jumlah_pengeluaran', 'bukti']
        # exclude = ['estimasi_hasil','dana_terkumpul','status','luas_lahan',]