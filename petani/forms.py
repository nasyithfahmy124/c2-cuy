from django import forms
from .models import *

class FormDonasi(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['petani']