# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('textjokes', '0008_auto_20150410_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('joke', models.ForeignKey(related_name='comments', blank=True, to='textjokes.TextJoke', null=True)),
                ('punch_line', models.ForeignKey(related_name='comments', blank=True, to='textjokes.TextPunchline', null=True)),
                ('user', models.ForeignKey(related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Joke Comment',
                'verbose_name_plural': 'Joke Comments',
            },
            bases=(models.Model,),
        ),
    ]
