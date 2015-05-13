import math
from datetime import datetime, timedelta, time

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from django_extensions.management.jobs import BaseJob

from textjokes.models import TextJoke
from trend.models import TrendBaseline, TrendingJoke


TOP_TRENDS_NUMBER = settings.TOP_TRENDS_NUMBER


def get_trend_period(duration):
    today = timezone.now().date()
    period_epoch = today - timedelta(days=duration)
    tomorrow = today + timedelta(days=1)
    time_period_start = datetime.combine(period_epoch, time())
    time_period_end = datetime.combine(tomorrow, time())
    return time_period_start, time_period_end


class ZScore:
    """See: http://stackoverflow.com/a/826509/2074794
    """

    def __init__(self, decay, pop=[]):
        self.sqrAvg = self.avg = 0
        # The rate at which the historic data's effect will diminish.
        self.decay = float(decay)
        for x in pop:
            self.update(float(x))

    def update(self, value):
        # Set initial averages to the first value in the sequence.
        if self.avg == 0 and self.sqrAvg == 0:
            self.avg = float(value)
            self.sqrAvg = float((value ** 2))
        # Calculate the average of the rest of the values using a
        # floating average.
        else:
            self.avg = self.avg * self.decay + value * (1 - self.decay)
            self.sqrAvg = self.sqrAvg * self.decay + (value ** 2) * (
                1 - self.decay)
        return self

    def std(self):
        # Somewhat ad-hoc standard deviation calculation.
        return math.sqrt(self.sqrAvg - self.avg ** 2)

    def score(self, obs):
        if self.std() == 0:
            # 1e7 is used instead of infinity so it can be saved in DecimalField
            return (float(obs) - self.avg) * 1e7
        else:
            return (float(obs) - self.avg) / self.std()


class Job(BaseJob):
    help = "Update baseline for trends"

    def execute(self):
        trends = TrendBaseline.objects.all()
        for trend in trends:
            time_period_start, time_period_end = get_trend_period(trend.period)

            jokes = TextJoke.objects.filter(
                Q(updated__range=(time_period_start, time_period_end)) |
                Q(punchlines__updated__range=(
                    time_period_start, time_period_end)) |
                Q(joke_votes__updated__range=(
                    time_period_start, time_period_end)) |
                Q(comments__updated__range=(
                    time_period_start, time_period_end)
                  )
            ).distinct().order_by('updated')
            population = jokes.values_list('trend_weight', flat=True)
            zscore = ZScore(trend.decay_rate, population)
            scores = {}
            for joke in jokes:
                joke_score = zscore.score(joke.trend_weight)
                if len(scores) > TOP_TRENDS_NUMBER:
                    if joke_score >= min(scores.values()):
                        scores[joke.id] = joke_score
                else:
                    scores[joke.id] = joke_score
            TrendingJoke.objects.filter(
                ~Q(id__in=list(scores.keys()))).delete()
            for joke in scores:
                TrendingJoke.objects.update_or_create(
                    trend=trend, joke_id=joke,
                    defaults={'score': scores[joke]})
