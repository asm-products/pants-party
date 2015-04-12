# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ppuser', '0003_auto_20150324_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='set_profile',
            field=models.BooleanField(default=False, help_text=b'Has the user set up his profile.', verbose_name='set_profile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_verified',
            field=models.BooleanField(default=False, help_text='Designates whether the user has been verified via an email confirmation.', verbose_name='verified'),
            preserve_default=True,
        ),
    ]
