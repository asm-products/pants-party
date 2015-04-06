from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class BlogPost(models.Model):
    author      = models.ForeignKey(settings.AUTH_USER_MODEL)
    title       = models.CharField(max_length=255, null=False, blank=False)
    slug        = models.CharField(max_length=255, null=True, blank=True)
    body        = models.TextField()
    created     = models.DateTimeField(null=True, blank=True)
    header_img  = models.ImageField(upload_to="images/")

    def __unicode__(self):
        return "%s" % (self.title)

    class Meta:
        verbose_name        = "Blog Post"
        verbose_name_plural = "Blog Post"
