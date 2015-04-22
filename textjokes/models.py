from django.db import models
from django.conf import settings
from datetime import datetime
from uuslug import uuslug


class TextJokeCategory(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    num_jokes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuslug(self.name, instance=self)
        super(TextJokeCategory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Joke Category"
        verbose_name_plural = "Joke Categories"


class TextJoke(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='jokes')
    category = models.ForeignKey(TextJokeCategory, related_name='category', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    responses = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    score = models.IntegerField(default=1)

    @property
    def user_has_voted(self):
        return False

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return "%s - %s" % (self.user.username, self.text)


class TextPunchline(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_punchlines')
    joke = models.ForeignKey(TextJoke, null=False, blank=False, related_name='punchlines')
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255, blank=False)
    active = models.BooleanField(default=True)
    responses = models.IntegerField(default=0)
    score = models.IntegerField(default=1)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return "%s - %s" % (self.user.username, self.text)


class JokeVotes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_votes')
    joke = models.ForeignKey(TextJoke, null=False, blank=False, related_name='joke_votes')
    vote = models.IntegerField(default=0)
    ip_address = models.IPAddressField(null=True, blank=True)

    def __unicode__(self):
        return "%s : %s" % (self.user.username, self.vote)

    class Meta:
        unique_together = (("user", "joke"),)
        verbose_name = "Joke Vote"
        verbose_name_plural = "Joke Votes"


class TextComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='comments')
    joke = models.ForeignKey(TextJoke, null=True, blank=True,
                             related_name='comments')
    punch_line = models.ForeignKey(TextPunchline, null=True, blank=True,
                                   related_name='comments')
    text = models.CharField(max_length=255, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def comment_on(self):
        if self.punch_line:
            return 'punchline'
        else:
            return 'joke'
    
    def __unicode__(self):
        return self.user.username + ' commented: ' + self.text
        
    class Meta:
        verbose_name = "Joke Comment"
        verbose_name_plural = "Joke Comments"

# This is where the signal stuff belongs, I guess.
from rq import Queue
from redis import Redis
from worker import conn
from mailframework.mails import send_verify_email, send_welcome_email
from django.db.models.signals import post_save
from django.dispatch import receiver

redis_conn = Redis()
# try: 
    # q = Queue(connection=redis_conn)  # no args implies the default queue
# except Exception:
    # q = Queue(connection=conn)
q = Queue(connection=conn)

@receiver(post_save, sender=TextComment)
def handle(sender, instance, created, **kwargs):
    if created:
        print "Instance"
        if instance.joke:
            print "This belongs to a joke"
            print instance.joke
        if instance.punch_line:
            print "This belongs to a punchline"
            print instance.punch_line
