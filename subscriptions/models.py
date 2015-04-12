from django.db import models
from shortuuid import uuid
from datetime import datetime


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    uuid = models.CharField(max_length=22, null=True, blank=True)
    created = models.DateTimeField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    confirmed_on = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.now()

        if not self.uuid:
            self.uuid = uuid()

        super(Subscription, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s" % (self.email)
