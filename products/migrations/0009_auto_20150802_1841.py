# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_orderprocess'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='lawyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='accounts.Lawyer', null=True),
        ),
    ]
