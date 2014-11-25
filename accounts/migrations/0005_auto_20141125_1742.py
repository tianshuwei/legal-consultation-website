# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyer',
            name='questions',
            field=models.ManyToManyField(related_name='c_l_questions', through='accounts.Question', to='accounts.Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lawyer',
            name='remarks',
            field=models.ManyToManyField(related_name='c_l_remarks', through='accounts.Remark', to='accounts.Client'),
            preserve_default=True,
        ),
    ]
