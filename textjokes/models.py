from django.db import models
from django.conf import settings
from datetime import datetime

class TextJoke(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='jokes')
    created         = models.DateTimeField(null=True, blank=True)
    text            = models.CharField(max_length=255, null=False, blank=False)
    active          = models.BooleanField(default=True)
    responses       = models.IntegerField(default=0)
    score           = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return "%s - %s" % (self.user.username, self.text) 

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.now()

        super(TextJoke, self).save(*args, **kwargs)

class TextPunchline(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_punchlines')
    joke            = models.ForeignKey(TextJoke, null=False, blank=False, related_name='punchlines')
    created         = models.DateTimeField(null=True, blank=True)
    text            = models.CharField(max_length=255, null=False, blank=False)
    active          = models.BooleanField(default=True)
    responses       = models.IntegerField(default=0)
    score           = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return "%s - %s" % (self.user.username, self.text) 

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.now()

        super(TextPunchline, self).save(*args, **kwargs)

