# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smartcontract', '0005_auto_20150328_1627'),
        ('products', '0017_auto_20150805_0144'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordercontract',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='smartcontract.SmartContract', null=True),
        ),
        migrations.AddField(
            model_name='ordercontract',
            name='instance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='smartcontract.SmartContractInstance', null=True),
        ),
    ]
