from django.db import models
from hashlib import sha256
import datetime

levels = (
    ('1', 'Standard User'),
    ('2', 'Supervisor'),
    ('3', 'Administrator')
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
    user_id = models.IntegerField(blank=False, editable=False)
    date = models.DateField(blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True)
    time_worked = models.CharField(max_length=4, default=0, blank=False)
    note = models.TextField(blank=True)


class Message(models.Model):
    message = models.TextField(blank=False)
    expire_date = models.DateTimeField(blank=False)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return "%s" % (self.message,)
