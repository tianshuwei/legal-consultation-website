# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20141124_1658'),
        ('accounts', '0005_auto_20141125_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='comments',
            field=models.ManyToManyField(related_name='c_p_comments', through='accounts.Comment', to='products.Product'),
            preserve_default=True,
        ),
    ]
