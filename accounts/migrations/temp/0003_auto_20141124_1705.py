# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141115_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='balance',
            field=models.DecimalField(default=0, max_digits=16, decimal_places=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='client',
            name='points',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='balance',
            field=models.DecimalField(default=0, max_digits=16, decimal_places=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='score',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
