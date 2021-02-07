from django import forms
from django.core.validators import RegexValidator, MaxLengthValidator
from . models import Project, Setting

numeric = RegexValidator(r'^[0-9+]', 'Only numeric characters.')
time_max_length = MaxLengthValidator(4, 'Length limit exceeds 4 characters')
max_daily_hours_length = MaxLengthValidator(2, 'Only 2 place values allowed')
session_timeout_length = MaxLengthValidator(4, 'Only 4 place values allowed')

hours = []
try:
    max_daily_hours = Setting.objects.get(setting='Max Daily Hours')
    for hour in range(0, int(max_daily_hours.value)+1):
        hours.append(("%i" % hour, "%i" % hour))
except Exception as e:
    print(e)
    for hour in range(0, 9):
        hours.append(("%i" % hour, "%i" % hour))


minutes = (
    ('0', '0'),
    ('0.25', '15'),
    ('0.50', '30'),
    ('0.75', '45')
)


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

    hours = forms.ChoiceField(required=True, choices=hours, widget=forms.Select(attrs={
        'class': 'form-control form-control-lg',
    }))

    minutes = forms.ChoiceField(required=True, choices=minutes, widget=forms.Select(attrs={
        'class': 'form-control form-control-lg',
    }))


class SettingsForm(forms.Form):
    max_daily_hours = forms.CharField(required=True, validators=[max_daily_hours_length])
    session_timeout = forms.CharField(required=True, validators=[session_timeout_length])
    allow_entry_edit = forms.BooleanField(required=True)

