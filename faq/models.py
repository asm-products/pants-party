from django.db import models
from datetime import datetime
from uuslug import uuslug


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    answer = models.TextField()
    created = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(null=True, blank=True)
    helpful_yes = models.IntegerField(default=0)
    helpful_no = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __unicode__(self):
        return "%s" % (self.question)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = datetime.now()
        self.updated = datetime.now()
        slug = uuslug(self.question, instance=self)
        super(FAQ, self).save(*args, **kwargs)
