# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('textjokes', '0007_auto_20150408_2121'),
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
        migrations.AlterModelOptions(
            name='jokevotes',
            options={'verbose_name': 'Joke Vote', 'verbose_name_plural': 'Joke Votes'},
        ),
        migrations.AlterModelOptions(
            name='textjokecategory',
            options={'verbose_name': 'Joke Category', 'verbose_name_plural': 'Joke Categories'},
        ),
        migrations.AlterField(
            model_name='textjokecategory',
            name='num_jokes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
