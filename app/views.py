from django.shortcuts import render, redirect
from . forms import LoginForm, CreateUserForm, TimeEntryForm, SettingsForm
from django.core.validators import ValidationError
from . models import User, Setting, Entry
from hashlib import sha256
import datetime


def hash_pin(pin):
    return sha256(pin.encode('utf-8')).hexdigest()


def get_user(uid):
    user = User.objects.get(id=uid)
    return user


def check_setup():
    settings = Setting.objects.all()
    if len(settings) > 0:
        return True
    else:
        return False


def logout_user(request):
    request.session['authenticated'] = False
    return redirect('home')


def requires_auth(request):
    auth = request.session.get('authenticated', None)
    if auth is True:
        return True
    else:
        return False


def setup(request):
    if check_setup() is True:
        return redirect('home')

    form = SettingsForm()

    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            s = Setting()
            s.setting = 'Max Daily Hours'
            s.value = data['max_daily_hours']
            s.save()

            s = Setting()
            s.setting = 'Session Timeout'
            s.value = data['session_timeout']
            s.save()

            s = Setting()
            s.setting = 'Max Daily Entries'
            s.value = data['max_daily_entries']
            s.save()

            s = Setting()
            s.setting = 'Projects'
            s.value = data['projects']
            s.save()

            return redirect('home')

    context = {
        'form': form
    }

    return render(request, 'setup.html', context=context)


def create_user(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            users = User.objects.filter(pin=hash_pin(data['pin']))
            if len(users) == 0:
                user = User()
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.pin = data['pin']
                user.save()
                return redirect('timesheet')
            else:
                form.add_error('pin', 'PIN already exists')

    context = {
        'form': form
    }

    return render(request, 'create_user.html', context=context)


def home(request):
    if check_setup() is False:
        return redirect('setup')
    form = LoginForm
    login_error = False
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            pin = sha256(data['pin'].encode('utf-8')).hexdigest()
            user = User.objects.filter(pin=pin, status=True).first()
            if user is None:
                form.add_error('pin', 'Invalid login')
                login_error = True
            else:
                request.session['authenticated'] = True
                request.session['uid'] = user.id
                return redirect('timesheet')

    context = {
        'form': form,
        'login_error': login_error
    }

    return render(request, 'home.html', context=context)


def timesheet(request):
    if requires_auth(request) is False:
        request.session['authenticated'] = False
        return redirect('home')

    uid = request.session.get('uid')
    user = get_user(uid)

    projects = Setting.objects.get(setting='Projects')

    form = TimeEntryForm()

    if request.method == "POST":
        form = TimeEntryForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            if data['hours'] == '0' and data['minutes'] == '0':
                form.add_error('hours', 'May not be 0 if minutes is 0')
                form.add_error('minutes', 'May not be 0 if hours is 0')
            else:
                entry = Entry()
                entry.user = user
                entry.project = data['project']
                entry.date = datetime.datetime.now().date()
                entry.hours = data['hours']
                entry.minutes = data['minutes']
                entry.save()
                form = TimeEntryForm()

    entries = Entry.objects.filter(user=user, date__month=datetime.datetime.now().month)

    date = datetime.datetime.now()
    max_daily_entries = Setting.objects.get(setting='Max Daily Entries')
    todays_entries = Entry.objects.filter(user=user, date=date).count()

    max_daily_entries_quota = False

    if int(todays_entries) >= int(max_daily_entries.value):
        max_daily_entries_quota = True

    time_entries = list()
    total_time_worked = 0
    for entry in entries:
        time_worked = float(entry.hours) + float(entry.minutes)
        e = {
            'id': entry.id,
            'date': entry.date,
            'hours': entry.hours,
            'minutes': entry.minutes,
            'project': entry.project,
            'time_worked': time_worked,
        }
        time_entries.append(e)
        total_time_worked = float(total_time_worked) + time_worked

    context = {
        'user': user,
        'form': form,
        'entries': time_entries,
        'total_time_worked': total_time_worked,
        'max_daily_entries_quota': max_daily_entries_quota,
        'projects': projects.value,
    }

    return render(request, 'timesheet.html', context=context)
