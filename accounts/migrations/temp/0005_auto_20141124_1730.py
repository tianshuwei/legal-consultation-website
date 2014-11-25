# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_lawyer_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawyer',
            name='remarks',
            field=models.ManyToManyField(to='accounts.Client', db_table=b'Remark'),
            preserve_default=True,
        ),
    ]
