from django.db import models
from django.conf import settings
from datetime import datetime
from uuslug import uuslug


class BlogPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=255, null=False, blank=False)
    slug = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()
    created = models.DateTimeField(null=True, blank=True)
    header_img = models.ImageField(upload_to="images/", null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.title)

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        if not self.created:
            self.created = datetime.now()

        return super(BlogPost, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Post"
