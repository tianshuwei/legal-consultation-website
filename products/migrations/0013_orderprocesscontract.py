# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartcontract', '0005_auto_20150328_1627'),
        ('products', '0012_auto_20150803_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProcessContract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='smartcontract.SmartContract', null=True)),
                ('orderprocess', models.ForeignKey(to='products.OrderProcess')),
            ],
        ),
    ]
