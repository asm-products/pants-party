# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import jsonfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider', models.CharField(max_length=20, verbose_name='provider', choices=[(b'facebook', b'facebook'), (b'twitter', b'twitter'), (b'reddit', b'reddit'), (b'google', b'google')])),
                ('access_token', models.TextField(null=True, verbose_name='access_token', blank=True)),
                ('other_token', models.CharField(max_length=255, null=True, verbose_name='other_token', blank=True)),
                ('display_name', models.CharField(max_length=50, verbose_name='display_name')),
                ('uid', models.CharField(max_length=50, verbose_name='uid')),
                ('extra_data', jsonfield.fields.JSONField(verbose_name='extra_data')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Social User',
                'verbose_name_plural': 'Social Users',
            },
            bases=(models.Model,),
        ),
    ]
