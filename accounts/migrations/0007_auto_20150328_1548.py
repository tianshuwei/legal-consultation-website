# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20150325_1844'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyer',
            name='intro',
            field=models.TextField(verbose_name='\u4e2a\u4eba\u4ecb\u7ecd', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lawyer',
            name='job_title',
            field=models.CharField(max_length=25, verbose_name='\u804c\u79f0', blank=True),
            preserve_default=True,
        ),
    ]
