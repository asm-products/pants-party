# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('textjokes', '0011_textjoke_comment_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='textcomment',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 12, 21, 41, 31, 867642, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='textjoke',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 12, 21, 41, 35, 687148, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='textpunchline',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 12, 21, 41, 40, 275979, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
