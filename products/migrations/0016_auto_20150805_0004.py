# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartcontract', '0005_auto_20150328_1627'),
        ('products', '0015_ordercontract'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercontract',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='smartcontract.SmartContractInstance', null=True),
        ),
        migrations.AlterField(
            model_name='ordercontract',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='smartcontract.SmartContract', null=True),
        ),
    ]
