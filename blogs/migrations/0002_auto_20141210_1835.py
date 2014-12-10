# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogsettings',
            name='lawyer',
            field=models.OneToOneField(to='accounts.Lawyer'),
            preserve_default=True,
        ),
    ]
