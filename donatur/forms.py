from django import forms
from .models import Donasi,DonasiBarang

class FormDonasi(forms.ModelForm):
    class Meta:
        model = Donasi
        fields = ['jumlah']
    
class FormDonasiBarang(forms.ModelForm):
    class Meta:
        model = DonasiBarang
        fields = ['kebutuhan', 'nama_barang_custom', 'jumlah', 'deskripsi']

    def clean(self):
        cleaned_data = super().clean()
        kebutuhan = cleaned_data.get('kebutuhan')
        nama_barang_custom = cleaned_data.get('nama_barang_custom')

        if not kebutuhan and not nama_barang_custom:
            raise forms.ValidationError("Pilih barang dari daftar atau isi manual.")

        return cleaned_data
        