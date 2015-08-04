# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20150328_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawyer',
            name='avatar',
            field=models.ImageField(max_length=255, upload_to=b'avatar.lawyer/', null=True, verbose_name='\u5934\u50cf', blank=True),
            preserve_default=True,
        ),
    ]
