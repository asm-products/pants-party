# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='confirmed_on',
        ),
        migrations.AlterField(
            model_name='subscription',
            name='confirmed',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 18, 16, 20, 25, 69595, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
