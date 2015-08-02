# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150321_2344'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('publish_date', models.DateTimeField(auto_now=True)),
                ('state', models.IntegerField(default=0, choices=[(0, b'OPEN'), (1, b'CLOSED')])),
                ('client', models.ForeignKey(to='accounts.Client')),
                ('lawyer', models.ForeignKey(to='accounts.Lawyer', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question_text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_flag', models.IntegerField(default=0, choices=[(0, b'ANSWER'), (1, b'ASK')])),
                ('text', models.TextField()),
                ('publish_date', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(to='questions.Question')),
                ('replier', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
