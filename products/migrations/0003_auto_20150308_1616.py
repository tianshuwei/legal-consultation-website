# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20150308_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='serial',
            field=models.CharField(default=products.models.gen_order_serial, max_length=25, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='text',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
