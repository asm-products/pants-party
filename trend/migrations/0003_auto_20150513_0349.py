# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trend', '0002_auto_20150513_0336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trendingjoke',
            options={'ordering': ['-score']},
        ),
    ]
