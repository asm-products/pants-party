from django.conf import settings
from django.db import models

from uuslug import uuslug


TREND_WEIGHTS = settings.TREND_WEIGHTS

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
    category = models.ForeignKey(TextJokeCategory, related_name='category',
                                 null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    responses = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    score = models.IntegerField(default=1)
    updated = models.DateTimeField(auto_now=True)
    trend_weight = models.DecimalField(default=0, max_digits=10,
                                       decimal_places=1, blank=True, null=True)

    @property
    def user_has_voted(self):
        return False

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return "%s - %s" % (self.user.username, self.text)

    def update_observation_weight(self, call_save=True):
        self.trend_weight = \
            TREND_WEIGHTS['punchline'] * len(self.punchlines.all()) + \
            TREND_WEIGHTS['score'] * self.score + \
            TREND_WEIGHTS['comment'] * len(self.comments.all()) + \
            TREND_WEIGHTS['vote'] * len(self.joke_votes.all())
        if call_save:
            self.save()

    def save(self, *args, **kwargs):
        self.update_observation_weight(call_save=False)
        super(TextJoke, self).save(*args, **kwargs)


class TextPunchline(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='user_punchlines')
    joke = models.ForeignKey(TextJoke, null=False, blank=False,
                             related_name='punchlines')
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255, blank=False)
    active = models.BooleanField(default=True)
    responses = models.IntegerField(default=0)
    score = models.IntegerField(default=1)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return "%s - %s" % (self.user.username, self.text)

    def save(self, *args, **kwargs):
        super(TextPunchline, self).save(*args, **kwargs)
        self.joke.update_observation_weight()


class JokeVotes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='user_votes')
    joke = models.ForeignKey(TextJoke, null=False, blank=False,
                             related_name='joke_votes')
    vote = models.IntegerField(default=0)
    ip_address = models.IPAddressField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s : %s" % (self.user.username, self.vote)

    class Meta:
        unique_together = (("user", "joke"),)
        verbose_name = "Joke Vote"
        verbose_name_plural = "Joke Votes"

    def save(self, *args, **kwargs):
        super(JokeVotes, self).save(*args, **kwargs)
        self.joke.update_observation_weight()


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
    updated = models.DateTimeField(auto_now=True)

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

    def save(self, *args, **kwargs):
        super(TextComment, self).save(*args, **kwargs)
        self.joke.update_observation_weight()

# This is where the signal stuff belongs, I guess.
from rq import Queue
from redis import Redis
from worker import conn
from mailframework.mails import send_verify_email, send_welcome_email

redis_conn = Redis()
# try: 
# q = Queue(connection=redis_conn)  # no args implies the default queue
# except Exception:
# q = Queue(connection=conn)
q = Queue(connection=conn)


