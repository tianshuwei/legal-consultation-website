# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_orderprocesscontract'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdoc',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 4, 18, 45, 32, 360294), auto_now=True),
            preserve_default=False,
        ),
    ]
