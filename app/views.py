from django.shortcuts import render, redirect
from . forms import LoginForm
from . models import User
from hashlib import sha256
from django.core import serializers


def logout(request):
    try:
        del request.session['user']
    except Exception as e:
        print(e)

    return redirect('home')


def secure_page(request):
    try:
        session_user = serializers.deserialize('json', request.session.get('u'))
        print(session_user)
        user = User.objects.filter(pin=session_user.pin).first()
        if user:
            return True
        else:
            del request.session['u']
            return redirect('home')
    except Exception as e:
        print(e)

    return redirect('home')


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


@secure_page
def timesheet(request):

    context = {

    }

    return render(request, 'timesheet.html', context=context)
