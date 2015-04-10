# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_faq_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='slug',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='faq',
            name='helpful_no',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='faq',
            name='helpful_yes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
