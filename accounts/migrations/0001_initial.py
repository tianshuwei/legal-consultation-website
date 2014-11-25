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
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.DecimalField(default=0, max_digits=16, decimal_places=3)),
                ('points', models.IntegerField(default=0)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lawyer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('balance', models.DecimalField(default=0, max_digits=16, decimal_places=3)),
                ('blacklist', models.BooleanField(default=False)),
                ('score', models.IntegerField(default=0)),
                ('blog', models.URLField(max_length=512)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade', models.IntegerField(default=0)),
                ('publish_date', models.DateTimeField(auto_now=True, verbose_name=b'date published')),
                ('client', models.ForeignKey(to='accounts.Client')),
                ('lawyer', models.ForeignKey(to='accounts.Lawyer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='lawyer',
            name='remarks',
            field=models.ManyToManyField(to='accounts.Client', through='accounts.Remark'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lawyer',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
