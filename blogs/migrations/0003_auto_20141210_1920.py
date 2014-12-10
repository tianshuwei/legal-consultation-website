# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20141210_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogsettings',
            name='items_per_page',
            field=models.IntegerField(default=15),
            preserve_default=True,
        ),
    ]
