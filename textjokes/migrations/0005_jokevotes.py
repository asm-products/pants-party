# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('textjokes', '0004_auto_20150324_2055'),
    ]

    operations = [
        migrations.CreateModel(
            name='JokeVotes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.IntegerField(default=0)),
                ('ip_address', models.IPAddressField(null=True, blank=True)),
                ('joke', models.ForeignKey(related_name='joke_votes', to='textjokes.TextJoke')),
                ('user', models.ForeignKey(related_name='user_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
