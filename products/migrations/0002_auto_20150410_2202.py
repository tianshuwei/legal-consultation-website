# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='include_html',
            field=models.CharField(default=0, max_length=255, verbose_name='\u9759\u6001html\u9875\u9762\u6a21\u677f\u8def\u5f84'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='publish_date',
            field=models.DateTimeField(auto_now=True, verbose_name='\u8bc4\u8bba\u65e5\u671f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='\u6b63\u6587'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u521b\u5efa\u65e5\u671f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='serial',
            field=models.CharField(default=products.models.gen_order_serial, verbose_name='\u8ba2\u5355\u53f7', max_length=25, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.IntegerField(default=0, verbose_name='\u8ba2\u5355\u72b6\u6001', choices=[(1, b'IN_BUSINESS'), (0, b'UNPAID'), (2, b'FINISHED'), (3, b'CANCELLED')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='text',
            field=models.TextField(verbose_name='\u8ba2\u5355\u5907\u6ce8', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='\u4ea7\u54c1\u63cf\u8ff0', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, verbose_name='\u4ea7\u54c1\u540d\u79f0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(default=0, verbose_name='\u5b9a\u4ef7', max_digits=16, decimal_places=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u53d1\u5e03\u65e5\u671f'),
            preserve_default=True,
        ),
    ]
