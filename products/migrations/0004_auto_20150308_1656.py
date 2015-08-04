# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20150308_1616'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': '\u8ba2\u5355', 'verbose_name_plural': '\u8ba2\u5355'},
        ),
        migrations.AlterField(
            model_name='order',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='accounts.Client', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='lawyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='accounts.Lawyer', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='products.Product', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='state',
            field=models.IntegerField(default=0, choices=[(1, b'IN_BUSINESS'), (0, b'UNPAID'), (2, b'FINISHED'), (3, b'CANCELLED')]),
            preserve_default=True,
        ),
    ]
