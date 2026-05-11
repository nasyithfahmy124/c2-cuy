from django import forms
from .models import Donasi,DonasiBarang
from django.forms import inlineformset_factory
from .models import DonasiBarang, DonasiBarangItem
from petani.models import KebutuhanBarang


class FormDonasi(forms.ModelForm):
    class Meta:
        model = Donasi
        fields = ['jumlah']
    
# class FormDonasiBarang(forms.ModelForm):
#     class Meta:
#         model = DonasiBarang
#         fields = ['kebutuhan', 'nama_barang_custom', 'jumlah', 'deskripsi']

#     def clean(self):
#         cleaned_data = super().clean()
#         kebutuhan = cleaned_data.get('kebutuhan')
#         nama_barang_custom = cleaned_data.get('nama_barang_custom')

#         if not kebutuhan and not nama_barang_custom:
#             raise forms.ValidationError("Pilih barang dari daftar atau isi manual.")

#         return cleaned_data
        

class FormDonasiBarang(forms.ModelForm):
    class Meta:
        model = DonasiBarang
        fields = []  # kosong (atau tambah catatan kalau mau)

class FormDonasiBarangItem(forms.ModelForm):

    class Meta:
        model = DonasiBarangItem
        fields = ['kebutuhan', 'jumlah']

        widgets = {
            'kebutuhan': forms.Select(attrs={
                'class': 'form-control'
            }),

            'jumlah': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
        }

    def __init__(self, *args, **kwargs):

        project = kwargs.pop('project', None)

        super().__init__(*args, **kwargs)

        if project:

            self.fields['kebutuhan'].queryset = (
                KebutuhanBarang.objects.filter(project=project)
            )

    def clean(self):

        cleaned_data = super().clean()

        instance = self.instance

        instance.kebutuhan = cleaned_data.get('kebutuhan')
        instance.jumlah = cleaned_data.get('jumlah')

        instance.clean()

        return cleaned_data

DonasiBarangItemFormSet = inlineformset_factory(
    DonasiBarang,
    DonasiBarangItem,
    form=FormDonasiBarangItem,
    extra=1,        
    can_delete=True 
)