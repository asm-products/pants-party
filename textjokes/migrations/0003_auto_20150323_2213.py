# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('textjokes', '0002_auto_20150323_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextPunchline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('text', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('responses', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=1)),
                ('joke', models.ForeignKey(to='textjokes.TextJoke')),
                ('user', models.ForeignKey(related_name='punchlines', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='textjoke',
            options={'ordering': ['-id']},
        ),
    ]
