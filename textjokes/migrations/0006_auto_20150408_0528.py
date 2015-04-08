# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textjokes', '0005_jokevotes'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='jokevotes',
            unique_together=set([('user', 'joke')]),
        ),
    ]
