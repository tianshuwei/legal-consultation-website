# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20150805_0004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordercontract',
            name='contract',
        ),
        migrations.RemoveField(
            model_name='ordercontract',
            name='instance',
        ),
    ]
