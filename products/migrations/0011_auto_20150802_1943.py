# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20150802_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='serial',
            field=models.CharField(default=products.models.gen_order_serial, verbose_name='\u8ba2\u5355\u53f7', unique=True, max_length=25, editable=False),
        ),
    ]
