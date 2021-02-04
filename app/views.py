from django.shortcuts import render


def home(request):

    context = {
        'title': 'Login',
    }

    return render(request, 'home.html', context=context)


def timesheet(request):

    context = {
        'title': 'Timesheet',
    }

    return render(request, 'timesheet.html', context=context)
