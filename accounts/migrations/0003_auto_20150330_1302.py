# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150328_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyer',
            name='intro',
            field=models.TextField(default='null', verbose_name='\u4e2a\u4eba\u4ecb\u7ecd', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lawyer',
            name='job_title',
            field=models.CharField(default='null', max_length=25, verbose_name='\u804c\u79f0', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='client',
            name='avatar',
            field=models.ImageField(max_length=255, upload_to=b'avatar.client/', null=True, verbose_name='\u5934\u50cf', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='balance',
            field=models.DecimalField(default=0, verbose_name='\u4f59\u989d', max_digits=16, decimal_places=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='points',
            field=models.IntegerField(default=0, verbose_name='\u79ef\u5206'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6ce8\u518c\u65e5\u671f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='avatar',
            field=models.ImageField(max_length=255, upload_to=b'avatar.lawyer/', null=True, verbose_name='\u5934\u50cf', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='balance',
            field=models.DecimalField(default=0, verbose_name='\u4f59\u989d', max_digits=16, decimal_places=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='blacklist',
            field=models.BooleanField(default=False, verbose_name='\u52a0\u5165\u9ed1\u540d\u5355'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6ce8\u518c\u65e5\u671f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='remark',
            name='grade',
            field=models.IntegerField(default=0, verbose_name='\u8bc4\u5206'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='remark',
            name='publish_date',
            field=models.DateTimeField(auto_now=True, verbose_name='\u8bc4\u5206\u65e5\u671f'),
            preserve_default=True,
        ),
    ]
