# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ppuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='display_name',
            field=models.CharField(max_length=254, null=True, verbose_name='display_name', blank=True),
            preserve_default=True,
        ),
    ]
