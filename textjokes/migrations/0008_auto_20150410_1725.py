# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textjokes', '0007_auto_20150408_2121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jokevotes',
            options={'verbose_name': 'Joke Vote', 'verbose_name_plural': 'Joke Votes'},
        ),
        migrations.AlterModelOptions(
            name='textjokecategory',
            options={'verbose_name': 'Joke Category', 'verbose_name_plural': 'Joke Categories'},
        ),
        migrations.AddField(
            model_name='textjokecategory',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='textjokecategory',
            name='num_jokes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
