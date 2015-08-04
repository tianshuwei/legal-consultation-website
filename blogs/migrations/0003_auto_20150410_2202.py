# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20150328_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogarticle',
            name='clicks',
            field=models.IntegerField(default=0, verbose_name='\u70b9\u51fb\u91cf', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='modify_date',
            field=models.DateTimeField(auto_now=True, verbose_name='\u4fee\u6539\u65e5\u671f', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u53d1\u8868\u65e5\u671f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='tags',
            field=models.CharField(max_length=255, verbose_name='\u6807\u7b7e', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='text',
            field=models.TextField(verbose_name='\u6b63\u6587'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='title',
            field=models.CharField(max_length=255, verbose_name='\u6587\u7ae0\u6807\u9898'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='name',
            field=models.CharField(max_length=255, verbose_name='\u5206\u7c7b\u540d\u79f0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='state',
            field=models.IntegerField(default=0, verbose_name='\u5206\u7c7b\u72b6\u6001', choices=[(0, b'PUBLIC'), (1, b'PRIVATE'), (-1, b'SYSTEM')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='publish_date',
            field=models.DateTimeField(auto_now=True, verbose_name='\u8bc4\u8bba\u65e5\u671f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='text',
            field=models.TextField(verbose_name='\u6b63\u6587'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogsettings',
            name='items_per_page',
            field=models.IntegerField(default=15, verbose_name='\u6bcf\u9875\u663e\u793a\u6587\u7ae0'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogsettings',
            name='state',
            field=models.IntegerField(default=0, verbose_name='\u535a\u5ba2\u72b6\u6001', choices=[(1, b'DISABLE'), (0, b'PUBLIC')]),
            preserve_default=True,
        ),
    ]
