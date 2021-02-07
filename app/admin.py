from django.contrib import admin
from . models import User, Project, Message, Entry, Setting, EntryNote
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'status']
    search_fields = ('last_name', 'first_name')
    ordering = ['last_name', 'first_name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    ordering = ['name']


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    pass


@admin.register(EntryNote)
class EntryNoteAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    readonly_fields = ['setting']
    ordering = ['setting']
    list_display = ['setting', 'value']
