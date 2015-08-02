# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartcontract', '0003_auto_20150325_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartcontract',
            name='template',
            field=models.FileField(max_length=255, null=True, upload_to=b'smart/', blank=True),
            preserve_default=True,
        ),
    ]
