from django import forms
from .models import *

class FormDonasi(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['petani','estimasi_hasil','dana_terkumpul','status','keuntungan_p']
class FormLaporan(forms.ModelForm):
    class Meta:
        model = Laporan
        fields = ['judul', 'deskripsi', 'jumlah_pengeluaran', 'bukti']
        
class formhasilpanen(forms.ModelForm):
    class Meta:
        model = HasilPanen
        fields = ['total_pendapatan','keterangan','bukti_panen',]
        