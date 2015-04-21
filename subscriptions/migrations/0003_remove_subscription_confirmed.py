# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_auto_20150418_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='confirmed',
        ),
    ]
