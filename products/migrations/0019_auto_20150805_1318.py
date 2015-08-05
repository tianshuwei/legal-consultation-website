# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20150805_0145'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ordercontract',
            unique_together=set([('order', 'contract')]),
        ),
    ]
