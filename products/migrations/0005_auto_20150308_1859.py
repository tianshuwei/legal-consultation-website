# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20150308_1656'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': '\u4ea7\u54c1', 'verbose_name_plural': '\u4ea7\u54c1'},
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
