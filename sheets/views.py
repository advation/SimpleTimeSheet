from django.shortcuts import render


def timesheet(request):

    context = {
        'title': 'Timesheet',
    }

    return render(request, 'timesheet.html', context=context)

