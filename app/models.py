from django.db import models
from hashlib import sha256
import uuid

levels = (
    ('1', 'Standard User'),
    ('2', 'Supervisor'),
    ('3', 'Administrator')
)

entry_status = (
    ('current', 'Current'),
    ('historical', 'historical')
)


class User(models.Model):
    status = models.BooleanField(default=True, blank=True)
    first_name = models.CharField(max_length=255, default="", blank=False)
    last_name = models.CharField(max_length=255, default="", blank=False)
    pin = models.CharField(max_length=255, null=False, blank=False, unique=True)
    level = models.CharField(max_length=255, blank=False, default="1", choices=levels)

    def save(self, *args, **kwargs):
        # Compare old vs new
        if self.pk:
            obj = User.objects.values('pin').get(pk=self.pk)
            if obj['pin'] != self.pin:
                self.pin = sha256(self.pin.encode('utf-8')).hexdigest()
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return "%s, %s (Enabled: %s)" % (self.last_name, self.first_name, self.status)


class Project(models.Model):
    name = models.CharField(blank=False, max_length=50, default="")
    description = models.TextField()

    def __str__(self):
        return "%s" % (self.name,)


class Entry(models.Model):
    uid = models.CharField(max_length=255, blank=False, default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None, null=True)
    date = models.DateField(blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    hours = models.CharField(max_length=2, default=0, blank=False)
    minutes = models.CharField(max_length=4, default=0, blank=False)
    status = models.CharField(default="", max_length=255, blank=False, choices=entry_status)
    validated = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return "%s, %s %s" % (self.date, self.user.last_name, self.user.first_name)

    class Meta:
        verbose_name_plural = "Time Entries"


class EntryNote(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    note = models.TextField(blank=False)

    def __str__(self):
        return "%s %s, %s - %s" % (self.entry.date, self.entry.user.last_name, self.entry.user.first_name, self.note)

    class Meta:
        verbose_name_plural = "Time Entry Notes"


class Message(models.Model):
    message = models.TextField(blank=False)
    expire_date = models.DateTimeField(blank=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return "%s" % (self.message,)


class Setting(models.Model):
    setting = models.CharField(max_length=255, blank=False, default="")
    value = models.CharField(max_length=255, blank=False, default="")

    def __str__(self):
        return "%s" % (self.setting,)