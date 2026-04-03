from django import forms
from .models import Donasi

class FormDonasi(forms.ModelForm):
    class Meta:
        model = Donasi
        fields = ['jumlah']
        