# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.CharField(max_length=255, null=True, blank=True)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('header_img', models.ImageField(upload_to=b'images/')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Blog Post',
                'verbose_name_plural': 'Blog Post',
            },
            bases=(models.Model,),
        ),
    ]
