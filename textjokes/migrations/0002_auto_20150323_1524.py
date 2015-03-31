# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('textjokes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textjoke',
            name='created',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='textjoke',
            name='user',
            field=models.ForeignKey(related_name='jokes', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
