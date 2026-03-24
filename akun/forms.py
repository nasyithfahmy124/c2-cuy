from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Register(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={
            "placeholder": "Masukkan email"
        })
    )

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            "placeholder": "Masukkan username"
        })
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Masukkan password"
        }),
        help_text=""  
    )

    password2 = forms.CharField(
        label="Konfirmasi Password",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Ulangi password"
        }),
        help_text=""  
        )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]