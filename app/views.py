from django.shortcuts import render, redirect
from . forms import LoginForm, CreateUserForm, TimeEntryForm
from . models import User
from hashlib import sha256


def hash_pin(pin):
    return sha256(pin.encode('utf-8')).hexdigest()


def logout_user(request):
    del request.session['authenticated']
    return redirect('home')


def requires_auth(request):
    return request.session.get('authenticated')


def get_user(uid):
    user = User.objects.get(id=uid)
    return user


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
    form = LoginForm
    login_error = False
    if request.method == "POST":
        form = LoginForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            pin = sha256(data['pin'].encode('utf-8')).hexdigest()
            user = User.objects.filter(pin=pin).first()
            print(user)
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
    if requires_auth(request):
        uid = request.session.get('uid')
        user = get_user(uid)

        form = TimeEntryForm()

        if request.method == "POST":
            form = TimeEntryForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print(data)

        context = {
            'user': user,
            'form': form,
        }

        return render(request, 'timesheet.html', context=context)
    else:
        request.session['authenticated'] = False
        return redirect('home')
