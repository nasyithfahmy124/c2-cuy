from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm

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

class GantiPwForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Password Lama",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan password lama'
        })
    )

    new_password1 = forms.CharField(
        label="Password Baru",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Masukkan password baru'
        }),
        help_text="Minimal 8 karakter"
    )

    new_password2 = forms.CharField(
        label="Konfirmasi Password Baru",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ulangi password baru'
        }),
        help_text="Masukkan ulang password baru."
    )

    error_messages = {
        'password_incorrect': "Password lama salah!",
        'password_mismatch': "Password baru tidak sama!",
    }