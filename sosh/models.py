from django.db import models
from django.utils import timezone
from django.conf import settings
# from .fields import JSONField
from jsonfield import JSONField
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

PROVIDERS = (
    ('facebook', 'facebook'),
    ('twitter', 'twitter'),
    ('reddit', 'reddit'),
    ('google', 'google'),
)


class SocialUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=False)
    provider = models.CharField(_('provider'), max_length=20, choices=PROVIDERS, null=False, blank=False)

    access_token = models.TextField(_('access_token'), null=True, blank=True)
    other_token = models.CharField(_('other_token'), max_length=255, null=True, blank=True)

    display_name = models.CharField(_('display_name'), max_length=50)
    uid = models.CharField(_('uid'), max_length=50, blank=False, null=False)
    extra_data = JSONField(_('extra_data'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    class Meta:
        verbose_name = _('Social User')
        verbose_name_plural = _('Social Users')

    def __unicode__(self):
        return "%s - %s" % (self.display_name, self.provider)

    def save(self, *args, **kwargs):
        if not self.date_joined:
            self.date_joined = datetime.now()

        return super(SocialUser, self).save(*args, **kwargs)
