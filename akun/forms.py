from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

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
    
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)