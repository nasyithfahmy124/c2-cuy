from django import forms
from edukasi.models import KategoriEdukasi,MateriEdukasi


class KategoriEdukasiForm(forms.ModelForm):
    class Meta:
        model = KategoriEdukasi
        fields = ['nama', 'icon', 'urutan']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nama kategori (contoh: Pertanian Dasar)'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contoh: ph-plant'
            }),
            'urutan': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Urutan tampil'
            }),
        }


class MateriEdukasiForm(forms.ModelForm):
    class Meta:
        model = MateriEdukasi
        fields = [
            'kategori',
            'judul',
            'konten',
            'target_role',
            'waktu_baca',
            'urutan'
        ]
        widgets = {
            'kategori': forms.Select(attrs={
                'class': 'form-control'
            }),
            'judul': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Judul materi'
            }),
            'konten': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Isi materi (bisa HTML)'
            }),
            'target_role': forms.Select(attrs={
                'class': 'form-control'
            }),
            'waktu_baca': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estimasi menit'
            }),
            'urutan': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Urutan materi'
            }),
        }