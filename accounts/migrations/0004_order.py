# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20141124_1658'),
        ('accounts', '0003_auto_20141125_1729'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.IntegerField(default=0)),
                ('text', models.TextField()),
                ('publish_date', models.DateTimeField(auto_now=True, verbose_name=b'date published')),
                ('client', models.ForeignKey(to='accounts.Client')),
                ('lawyer', models.ForeignKey(to='accounts.Lawyer')),
                ('product', models.ForeignKey(to='products.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
