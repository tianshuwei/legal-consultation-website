# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='serial',
            field=models.CharField(default='=========================', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='publish_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='publish_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='publish_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
