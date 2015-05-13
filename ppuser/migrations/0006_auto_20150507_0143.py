# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

import ppuser.models

class Migration(migrations.Migration):

    dependencies = [
        ('ppuser', '0005_customuser_verify_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_verified',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='verified_on',
            new_name='is_verified'
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(unique=True, max_length=254, verbose_name='email address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='verify_token',
            field=models.CharField(default=ppuser.models.get_uuid, max_length=22),
            preserve_default=True,
        ),
    ]
