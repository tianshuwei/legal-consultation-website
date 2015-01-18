# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=80)),
                ('serial', models.CharField(default=b'', max_length=20)),
                ('result', models.CharField(default=b'', max_length=20)),
                ('message', models.CharField(default=b'', max_length=120)),
                ('publish_date', models.DateTimeField(auto_now=True, verbose_name=b'date published')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
