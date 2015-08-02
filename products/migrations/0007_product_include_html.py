# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20150328_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='include_html',
            field=models.CharField(default='products/pages/Product_A.html', max_length=255, verbose_name='\u9759\u6001html\u9875\u9762\u6a21\u677f\u8def\u5f84'),
            preserve_default=False,
        ),
    ]
