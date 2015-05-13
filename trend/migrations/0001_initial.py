# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textjokes', '0013_auto_20150513_0246'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrendBaseline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.PositiveIntegerField(help_text=b'In days', verbose_name=b'Decay rate', choices=[(0, b'All time'), (1, b'Daily'), (30, b'Monthly'), (7, b'Weekly')])),
                ('decay_rate', models.DecimalField(decimal_places=2, default=0, max_digits=3, blank=0, help_text=b'between 0 and 1', null=0)),
            ],
            options={
                'verbose_name': 'Trend',
                'verbose_name_plural': 'Trends',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrendingJoke',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.DecimalField(max_digits=10, decimal_places=2)),
                ('joke', models.ForeignKey(to='textjokes.TextJoke')),
                ('trend', models.ForeignKey(to='trend.TrendBaseline')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='trendbaseline',
            name='trending_jokes',
            field=models.ManyToManyField(related_name='trends', null=True, through='trend.TrendingJoke', to='textjokes.TextJoke', blank=True),
            preserve_default=True,
        ),
    ]
