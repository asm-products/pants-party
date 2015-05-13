from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import TextComment


@receiver(post_save, sender=TextComment)
def handle_save(sender, instance, created, **kwargs):
    if created:
        if instance.joke:
            try:
                instance.joke.comment_count = instance.joke.comment_count + 1
                instance.joke.save()
            except Exception, e:
                print str(e)
        if instance.punch_line:
            # TODO - Implement counter for punchline
            print "This belongs to a punchline"
            print instance.punch_line


@receiver(pre_delete, sender=TextComment)
def handle_delete(sender, instance, **kwargs):
    if instance.joke:
        if not instance.joke.comment_count == 0:
            instance.joke.comment_count = instance.joke.comment_count - 1
            instance.joke.save()
    if instance.punch_line:
        # TODO - Implement counter for punchline
        print "This belongs to a punchline"
        print instance.punch_line
