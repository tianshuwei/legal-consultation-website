# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_siteactivity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteactivity',
            name='user',
        ),
        migrations.AddField(
            model_name='siteactivity',
            name='tags',
            field=models.CharField(default=b'', max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='message',
            field=models.CharField(max_length=120, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='publish_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='result',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='serial',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transactionrecord',
            name='title',
            field=models.CharField(default=b'', max_length=80, blank=True),
            preserve_default=True,
        ),
    ]
