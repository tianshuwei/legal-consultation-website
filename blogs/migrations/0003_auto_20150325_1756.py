# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20150308_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogarticle',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
    ]
