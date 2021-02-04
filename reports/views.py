from django.shortcuts import render


def reports(request):

    context = {
        'title': 'Reports',
    }

    return render(request, 'reports.html', context=context)
