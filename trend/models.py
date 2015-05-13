from django.conf import settings
from django.db import models


PERIODS = settings.TREND_PERIODS


class TrendBaseline(models.Model):
    period = models.PositiveIntegerField(
        'Decay rate', help_text='In days',
        choices=zip(PERIODS.keys(), PERIODS.values()))
    decay_rate = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True, default=0,
        help_text='between 0 and 1')
    trending_jokes = models.ManyToManyField(
        'textjokes.TextJoke', related_name='trends', null=True, blank=True,
        through='trend.TrendingJoke')

    def __unicode__(self):
        return PERIODS[self.period]

    def save(self, *args, **kwargs):
        if not self.decay_rate:
            self.decay_rate = 0
        super(TrendBaseline, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Trend'
        verbose_name_plural = 'Trends'


class TrendingJoke(models.Model):
    trend = models.ForeignKey(TrendBaseline)
    joke = models.ForeignKey('textjokes.TextJoke')
    score = models.DecimalField(max_digits=10, decimal_places=2)

    def __unicode__(self):
        return str(self.joke) + ': ' + str(self.score)

    class Meta:
        ordering = ['-score']
