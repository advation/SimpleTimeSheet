from django.shortcuts import render


def settings(request):

    context = {
        'title': 'Settings',
    }

    return render(request, 'settings.html', context=context)
