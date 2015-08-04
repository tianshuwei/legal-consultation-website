# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20150328_1502'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': '\u95ee\u9898\u54a8\u8be2', 'verbose_name_plural': '\u95ee\u9898\u54a8\u8be2'},
        ),
        migrations.AlterField(
            model_name='question',
            name='clicks',
            field=models.IntegerField(default=0, verbose_name='\u95ee\u9898\u70b9\u51fb\u91cf', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.TextField(verbose_name='\u95ee\u9898\u63cf\u8ff0', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u63d0\u95ee\u65e5\u671f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='state',
            field=models.IntegerField(default=0, verbose_name='\u95ee\u9898\u72b6\u6001', choices=[(0, b'OPEN'), (1, b'CLOSED')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=255, verbose_name='\u95ee\u9898\u6807\u9898'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question_text',
            name='publish_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u53d1\u5e03\u65e5\u671f'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question_text',
            name='text',
            field=models.TextField(verbose_name='\u6b63\u6587'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question_text',
            name='user_flag',
            field=models.IntegerField(default=0, verbose_name='\u8ffd\u95ee/\u56de\u7b54', choices=[(0, b'ANSWER'), (1, b'ASK')]),
            preserve_default=True,
        ),
    ]
