# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ppuser', '0006_auto_20150507_0143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_verified',
            field=models.DateTimeField(help_text='Designates when the user was verified via an email confirmation (null if not verified).', null=True, verbose_name='verified', blank=True),
            preserve_default=True,
        ),
    ]
