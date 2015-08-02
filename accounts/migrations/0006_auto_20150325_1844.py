# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_activity_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lawyer',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
