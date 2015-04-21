from django.db import models
from shortuuid import uuid


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    uuid = models.CharField(max_length=22, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid()

        super(Subscription, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.email
