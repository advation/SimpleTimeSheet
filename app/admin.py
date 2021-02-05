from django.contrib import admin
from . models import User
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'status']

