# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20150328_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='avatar',
            field=models.ImageField(max_length=255, null=True, upload_to=b'avatar.client/', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='points',
            field=models.IntegerField(default=0, verbose_name='\u79ef\u5206'),
            preserve_default=True,
        ),
    ]
