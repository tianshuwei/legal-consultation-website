# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('smartcontract', '0004_auto_20150328_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartcontract',
            name='config',
            field=models.TextField(verbose_name='\u5408\u540c\u8868\u5355\u8bbe\u8ba1', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smartcontract',
            name='name',
            field=models.CharField(max_length=255, verbose_name='\u5408\u540c\u540d\u79f0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smartcontract',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u521b\u5efa\u65e5\u671f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smartcontract',
            name='state',
            field=models.IntegerField(default=0, verbose_name='\u5408\u540c\u72b6\u6001', choices=[(0, b'DEFAULT')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smartcontract',
            name='template',
            field=models.FileField(max_length=255, upload_to=b'smart/', null=True, verbose_name='DOCX\u6a21\u677f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smartcontractcategory',
            name='name',
            field=models.CharField(max_length=120, verbose_name='\u5408\u540c\u5206\u7c7b\u540d\u79f0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smartcontractcategory',
            name='state',
            field=models.IntegerField(default=0, verbose_name='\u5408\u540c\u5206\u7c7b\u72b6\u6001', choices=[(0, b'PUBLIC')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smartcontractinstance',
            name='data',
            field=models.TextField(verbose_name='\u5408\u540c\u6570\u636e', blank=True),
            preserve_default=True,
        ),
    ]
