from django.db import models
from shortuuid import uuid


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    uuid = models.CharField(max_length=22, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    confirmed = models.DateTimeField(null=True, blank=True)

    @property
    def is_confirmed(self):
        # This method has the role of old 'confirmed' field, so we just use one
        # field instead of two.
        if self.confirmed:
            return True
        else: 
            return False
        # return bool(self.confirmed)

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = uuid()

        super(Subscription, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.email
