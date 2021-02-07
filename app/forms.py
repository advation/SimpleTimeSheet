from django import forms
from django.core.validators import RegexValidator, MaxLengthValidator, MinLengthValidator, ValidationError
from . models import Project, Setting

numeric = RegexValidator(r'^[0-9+]', 'Only numeric characters.')
time_max_length = MaxLengthValidator(4, 'Length limit exceeds 4 characters.')
max_daily_hours_length = MaxLengthValidator(2, 'Only 2 place values allowed.')
session_timeout_length = MaxLengthValidator(4, 'Only 4 place values allowed.')
min_pin_length = MinLengthValidator(4, 'Must be at least 4 characters long.')
max_pin_length = MaxLengthValidator(4, 'May not be longer then 4 characters long.')


def pin_blacklist(value):
    blacklist = ['1234', '4321', '0000', '1111',
                 '2222', '3333', '4444', '5555',
                 '6666', '7777', '8888', '9999',
                 '2345', '5432', '3456', '6543',
                 '4567', '7654', '5678', '8765',
                 '6789', '9876', '7890', '0987']
    if value in blacklist:
        raise ValidationError("Please provide a more complex PIN")
    else:
        return value


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
    pin = forms.CharField(strip=True, required=True, validators=[numeric, min_pin_length, max_pin_length, pin_blacklist],
                          help_text="4 character numeric PIN")


class TimeEntryForm(forms.Form):
    project = forms.ModelChoiceField(Project.objects.all(), required=False, label="Select a project if applicable (not required)",
                                     widget=forms.Select(attrs={'class': 'form-control form-control-lg'}))
    hours = forms.ChoiceField(required=True, choices=hours,
                              widget=forms.Select(attrs={'class': 'form-control form-control-lg'}))
    minutes = forms.ChoiceField(required=True, choices=minutes,
                                widget=forms.Select(attrs={'class': 'form-control form-control-lg'}))


class SettingsForm(forms.Form):
    max_daily_hours = forms.CharField(required=True, validators=[max_daily_hours_length])
    session_timeout = forms.CharField(required=True, validators=[session_timeout_length])
    allow_entry_edit = forms.BooleanField(required=True)

