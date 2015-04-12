# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ppuser', '0004_auto_20150410_0300'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='verify_token',
            field=models.CharField(max_length=22, null=True, blank=True),
            preserve_default=True,
        ),
    ]
