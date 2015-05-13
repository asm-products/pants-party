# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('textjokes', '0012_auto_20150512_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='jokevotes',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 13, 2, 46, 24, 169803, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='textjoke',
            name='trend_weight',
            field=models.DecimalField(default=0, null=True, max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
    ]
