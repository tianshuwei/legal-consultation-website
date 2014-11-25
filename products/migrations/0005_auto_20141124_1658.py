# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20141124_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(default=b'', max_length=256),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='publish_date',
            field=models.DateTimeField(auto_now=True, verbose_name=b'date published'),
            preserve_default=True,
        ),
    ]
