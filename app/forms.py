from django import forms
from django.core.validators import RegexValidator, MaxLengthValidator
from . models import Project

numeric = RegexValidator(r'^[0-9+]', 'Only numeric characters.')
time_max_length = MaxLengthValidator(4, 'Length limit exceeds 4 characters')


class LoginForm(forms.Form):
    pin = forms.CharField(strip=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg p-4 text-center',
        'id': 'pin',
        'placeholder': 'PIN',
    }), validators=[numeric])


class CreateUserForm(forms.Form):
    first_name = forms.CharField(strip=True, required=True)
    last_name = forms.CharField(strip=True, required=True)
    pin = forms.CharField(strip=True, required=True, validators=[numeric], help_text="Numeric values only")


class TimeEntryForm(forms.Form):
    project = forms.ModelChoiceField(Project.objects.all(), required=False, widget=forms.Select(attrs={
        'class': 'form-control form-control-lg'
    }))
    time_worked = forms.CharField(required=True, label="Hours Worked", widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg',
        'max-length': '4',
        'placeholder': 'Examples: 0.25, 1.5, 2'
    }), validators=[time_max_length, numeric])
