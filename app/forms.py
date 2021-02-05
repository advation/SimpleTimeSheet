from django import forms
from django.core.validators import RegexValidator

numeric = RegexValidator(r'^[0-9+]', 'Only numeric characters.')


class LoginForm(forms.Form):
    pin = forms.CharField(strip=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg p-4 text-center',
        'id': 'pin',
    }), label=None, validators=[numeric])
