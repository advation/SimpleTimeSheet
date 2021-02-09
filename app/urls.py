"""TimeSheet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('setup', views.setup, name='setup'),
    path('timesheet', views.timesheet, name="timesheet"),
    path('timesheet/<int:year>/<int:month>', views.timesheet, name="timesheet"),
    path('timesheet/<int:year>/<int:month>/<int:day>', views.timesheet, name="timesheet"),
    path('logout', views.logout_user, name="logout"),
    path('create/user', views.create_user, name="create_user"),
    path('remove/<int:entry_id>', views.remove, name='remove_entry'),
    path('edit/<int:entry_id>', views.edit, name='edit_entry'),
]
