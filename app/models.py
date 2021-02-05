from django.db import models


# Create your models here.
class User(models.Model):
    status = models.BooleanField(default=True, blank=True)
    first_name = models.CharField(max_length=255, default="", blank=False)
    last_name = models.CharField(max_length=255, default="", blank=False)
    pin = models.CharField(max_length=255, default="", blank=False, unique=True)

    def __str__(self):
        return "%s, %s (Enabled: %s)" % (self.last_name, self.first_name, self.status)
