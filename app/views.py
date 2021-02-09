from django.shortcuts import render, redirect
from . forms import LoginForm, CreateUserForm, TimeEntryForm, SettingsForm, PastTimeEntryForm
from . models import User, Setting, Entry
from hashlib import sha256
import datetime
from django.template.defaultfilters import date
from dateutil.relativedelta import relativedelta


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

    auth_timeout = int(Setting.objects.get(setting="Session Timeout").value) * 60
    context = {
        'form': form,
        'auth_timeout': auth_timeout
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


def timesheet(request, year=None, month=None, day=None):
    date = datetime.datetime.now()

    if year is None:
        year = date.year

    if month is None:
        month = date.month

    if month > 12:
        return redirect('timesheet', year=year, month=12)

    if day is None:
        day = date.day

    if datetime.date(year=year, month=month, day=day) <= datetime.date.today():
        show_form = True
    else:
        show_form = False

    if datetime.date(year=year, month=month, day=day) < datetime.date.today():
        show_next = True
    else:
        show_next = False

    if datetime.date(year=year, month=month, day=day) == datetime.date.today():
        today_is_today = True
    else:
        today_is_today = False

    current_month = datetime.date(year, month, 1)
    next_month = current_month + relativedelta(months=+1)
    previous_month = current_month + relativedelta(months=-1)

    if requires_auth(request) is False:
        request.session['authenticated'] = False
        return redirect('home')

    uid = request.session.get('uid')
    user = get_user(uid)

    projects = Setting.objects.get(setting='Projects')

    if today_is_today:
        form = TimeEntryForm()
    else:
        form = PastTimeEntryForm(month=current_month.month, year=current_month.year)

    if request.method == "POST":
        # form = TimeEntryForm(request.POST)

        if today_is_today:
            form = TimeEntryForm(request.POST)
        else:
            form = PastTimeEntryForm(request.POST, month=current_month.month, year=current_month.year)

        if form.is_valid():
            data = form.cleaned_data
            if data['hours'] == '0' and data['minutes'] == '0':
                form.add_error('hours', 'May not be 0 if minutes is 0')
                form.add_error('minutes', 'May not be 0 if hours is 0')
            else:
                entry = Entry()
                entry.user = user
                entry.project = data['project']
                entry.date = datetime.date(year=current_month.year, month=current_month.month, day=current_month.day)
                entry.hours = data['hours']
                entry.minutes = data['minutes']
                entry.save()

                # form = TimeEntryForm()

                if today_is_today:
                    form = TimeEntryForm()
                else:
                    form = PastTimeEntryForm(month=current_month.month, year=current_month.year)

    entries = Entry.objects.filter(user=user, date__year=current_month.year, date__month=current_month.month)

    max_daily_entries = Setting.objects.get(setting='Max Daily Entries')
    todays_entries = Entry.objects.filter(user=user, date__year=current_month.year, date__month=current_month.month).count()

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

    auth_timeout = int(Setting.objects.get(setting="Session Timeout").value) * 60

    context = {
        'user': user,
        'form': form,
        'entries': time_entries,
        'show_form': show_form,
        'show_next': show_next,
        'today_is_today': today_is_today,
        'total_time_worked': total_time_worked,
        'max_daily_entries_quota': max_daily_entries_quota,
        'projects': projects.value,
        'session_timeout': auth_timeout,
        'current_month': current_month,
        'current_month_name': current_month.strftime('%B'),
        'next_month': next_month,
        'previous_month': previous_month,
    }

    return render(request, 'timesheet.html', context=context)


def remove(request, entry_id):
    if requires_auth(request) is False:
        request.session['authenticated'] = False
        return redirect('home')

    uid = request.session.get('uid')
    user = get_user(uid)

    entry = Entry.objects.filter(id=entry_id, user=user)
    entry.delete()
    return redirect('timesheet')


def edit(request, entry_id):
    if requires_auth(request) is False:
        request.session['authenticated'] = False
        return redirect('home')

    uid = request.session.get('uid')
    user = get_user(uid)

    form = TimeEntryForm()

    if request.method == "POST":
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['hours'] == '0' and data['minutes'] == '0':
                form.add_error('hours', 'Hours and Minutes may not be both 0')
                form.add_error('minutes', 'Hours and Minutes may not be both 0')
            else:
                entry = Entry.objects.filter(id=entry_id, user=user).first()
                entry.hours = data['hours']
                entry.minutes = data['minutes']
                entry.project = data['project']
                entry.save()

                return redirect('timesheet')

    entry = Entry.objects.filter(id=entry_id, user=user).first()
    projects = Setting.objects.get(setting="Projects")
    auth_timeout = int(Setting.objects.get(setting="Session Timeout").value) * 60

    if entry:
        form.fields['hours'].initial = entry.hours
        form.fields['minutes'].initial = entry.minutes
        if projects.value == "True":
            form.fields['project'].initial = entry.project
        else:
            del form.fields['project']
    else:
        return redirect('timesheet')

    context = {
        'form': form,
        'user': user,
        'entry': entry,
        'projects': projects.value,
        'session_timeout': auth_timeout
    }

    return render(request, 'edit.html', context=context)

