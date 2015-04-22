# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textjokes', '0010_auto_20150419_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='textjoke',
            name='comment_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
