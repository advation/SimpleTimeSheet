from django.shortcuts import render, redirect
from . forms import LoginForm
from . models import User
from hashlib import sha256
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm


def logout_user(request):
    logout(request)
    return redirect('home')


def create_user(request):
    form = CreateUserForm
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)

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
            print(pin)
            user = User.objects.filter(pin=pin)

            if user is None:
                form.add_error('pin', 'Invalid login')
                login_error = True
            else:
                request.session['u'] = serializers.serialize('json', user)
                return redirect('timesheet')

    context = {
        'form': form,
        'login_error': login_error
    }

    return render(request, 'home.html', context=context)


@login_required(login_url='/')
def timesheet(request):

    context = {

    }

    return render(request, 'timesheet.html', context=context)
