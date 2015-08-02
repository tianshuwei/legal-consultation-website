# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20150328_1600'),
        ('products', '0007_product_include_html'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProcess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lawyer', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='accounts.Lawyer', null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='products.Order', null=True)),
            ],
        ),
    ]
