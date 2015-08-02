# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartcontract', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smartcontractstep',
            name='contract',
        ),
        migrations.RemoveField(
            model_name='smartcontracttemplate',
            name='contract',
        ),
        migrations.DeleteModel(
            name='SmartContractTemplate',
        ),
        migrations.RemoveField(
            model_name='smartcontractvar',
            name='step',
        ),
        migrations.DeleteModel(
            name='SmartContractStep',
        ),
        migrations.DeleteModel(
            name='SmartContractVar',
        ),
        migrations.AlterModelOptions(
            name='smartcontract',
            options={'verbose_name': '\u5408\u540c\u6a21\u677f', 'verbose_name_plural': '\u5408\u540c\u6a21\u677f'},
        ),
        migrations.AlterModelOptions(
            name='smartcontractcategory',
            options={'verbose_name': '\u5408\u540c\u5206\u7c7b', 'verbose_name_plural': '\u5408\u540c\u5206\u7c7b'},
        ),
        migrations.AlterModelOptions(
            name='smartcontractinstance',
            options={'verbose_name': '\u5408\u540c\u5b9e\u4f8b', 'verbose_name_plural': '\u5408\u540c\u5b9e\u4f8b'},
        ),
        migrations.AddField(
            model_name='smartcontract',
            name='config',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='smartcontract',
            name='template',
            field=models.FileField(max_length=255, null=True, upload_to=b'smart/'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='smartcontractcategory',
            name='state',
            field=models.IntegerField(default=0, choices=[(0, b'PUBLIC')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smartcontract',
            name='name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smartcontract',
            name='publish_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smartcontract',
            name='state',
            field=models.IntegerField(default=0, choices=[(0, b'DEFAULT')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smartcontractcategory',
            name='name',
            field=models.CharField(max_length=120),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='smartcontractinstance',
            name='data',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
