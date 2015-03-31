# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('textjokes', '0003_auto_20150323_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textpunchline',
            name='joke',
            field=models.ForeignKey(related_name='punchlines', to='textjokes.TextJoke'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='textpunchline',
            name='user',
            field=models.ForeignKey(related_name='user_punchlines', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
