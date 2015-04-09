# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textjokes', '0006_auto_20150408_0528'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextJokeCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255, null=True, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('num_jokes', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='textjoke',
            name='category',
            field=models.ForeignKey(related_name='category', blank=True, to='textjokes.TextJokeCategory', null=True),
            preserve_default=True,
        ),
    ]
