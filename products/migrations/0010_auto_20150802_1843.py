# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20150802_1841'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='orderprocess',
            unique_together=set([('order', 'lawyer')]),
        ),
    ]
