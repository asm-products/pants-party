# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('textjokes', '0009_textcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textcomment',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 19, 22, 26, 36, 237037, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='textjoke',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 19, 22, 26, 46, 410934, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='textjokecategory',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 19, 22, 26, 54, 118122, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='textjokecategory',
            name='description',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='textpunchline',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 19, 22, 27, 25, 345605, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
