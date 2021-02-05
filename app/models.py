from django.db import models
from hashlib import sha256


# Create your models here.
class User(models.Model):
    status = models.BooleanField(default=True, blank=True)
    first_name = models.CharField(max_length=255, default="", blank=False)
    last_name = models.CharField(max_length=255, default="", blank=False)
    pin = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def save(self, *args, **kwargs):
        self.pin = sha256(self.pin.encode('utf-8')).hexdigest()

        user = User.objects.filter(pin=self.pin).first()
        if user:
            super(User, self).save(*args, **kwargs)

    def __str__(self):
        return "%s, %s (Enabled: %s)" % (self.last_name, self.first_name, self.status)
