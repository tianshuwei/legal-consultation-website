# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20150130_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogcategory',
            name='state',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
