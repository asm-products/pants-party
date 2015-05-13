# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trendbaseline',
            name='decay_rate',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3, blank=True, help_text=b'between 0 and 1', null=True),
            preserve_default=True,
        ),
    ]
