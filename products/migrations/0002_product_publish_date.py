# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 15, 10, 57, 11, 188862, tzinfo=utc), verbose_name=b'date published'),
            preserve_default=False,
        ),
    ]
