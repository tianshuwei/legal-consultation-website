# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20150802_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDoc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u6587\u6863\u6807\u9898', blank=True)),
                ('doc', models.FileField(max_length=255, upload_to=b'order/doc/')),
                ('order', models.ForeignKey(to='products.Order')),
            ],
        ),
        migrations.AlterField(
            model_name='orderprocess',
            name='order',
            field=models.ForeignKey(default=0, to='products.Order'),
            preserve_default=False,
        ),
    ]
