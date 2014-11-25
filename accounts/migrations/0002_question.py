# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=256)),
                ('description', models.TextField()),
                ('publish_date', models.DateTimeField(auto_now=True, verbose_name=b'date published')),
                ('client', models.ForeignKey(to='accounts.Client')),
                ('lawyer', models.ForeignKey(to='accounts.Lawyer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
