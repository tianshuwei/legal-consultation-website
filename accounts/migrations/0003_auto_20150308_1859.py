# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_question_state'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': '\u5ba2\u6237', 'verbose_name_plural': '\u5ba2\u6237'},
        ),
        migrations.AlterModelOptions(
            name='lawyer',
            options={'verbose_name': '\u5f8b\u5e08', 'verbose_name_plural': '\u5f8b\u5e08'},
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='publish_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='state',
            field=models.IntegerField(default=0, choices=[(0, b'OPEN'), (1, b'CLOSED')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question_text',
            name='publish_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='remark',
            name='publish_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
