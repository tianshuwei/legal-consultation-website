# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20141124_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyer',
            name='remarks',
            field=models.ManyToManyField(to='accounts.Client'),
            preserve_default=True,
        ),
    ]
