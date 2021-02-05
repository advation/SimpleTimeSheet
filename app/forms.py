from django import forms
from django.core.validators import RegexValidator
from . models import User

numeric = RegexValidator(r'^[0-9+]', 'Only numeric characters.')


class LoginForm(forms.Form):
    pin = forms.CharField(strip=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg p-4 text-center',
        'id': 'pin',
    }), label=None, validators=[numeric])


class UserForm(forms.Form):

    def clean(self):
        cleaned_data = self.cleaned_data
        pin = cleaned_data['pin']

        if pin and User.objects.get(pin=pin):
            raise forms.ValidationError("not unique")

        # Always return the full collection of cleaned data.
        return cleaned_data
    