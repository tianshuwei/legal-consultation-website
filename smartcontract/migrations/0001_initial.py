# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SmartContract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=255)),
                ('publish_date', models.DateTimeField(auto_now=True, verbose_name=b'date published')),
                ('state', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmartContractCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', unique=True, max_length=120)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmartContractInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.TextField()),
                ('contract', models.ForeignKey(to='smartcontract.SmartContract')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmartContractStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=30)),
                ('next_name', models.CharField(default=b'', max_length=30)),
                ('contract', models.ForeignKey(to='smartcontract.SmartContract')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmartContractTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('template_type', models.CharField(default=b'', max_length=32)),
                ('text', models.TextField()),
                ('state', models.IntegerField(default=0)),
                ('contract', models.ForeignKey(to='smartcontract.SmartContract')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmartContractVar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('widget', models.IntegerField(default=0)),
                ('extra', models.TextField()),
                ('name', models.CharField(default=b'', max_length=30)),
                ('label', models.CharField(default=b'', max_length=255)),
                ('help_text', models.CharField(default=b'', max_length=255)),
                ('next_name', models.CharField(default=b'', max_length=30)),
                ('step', models.ForeignKey(to='smartcontract.SmartContractStep')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='smartcontract',
            name='category',
            field=models.ForeignKey(to='smartcontract.SmartContractCategory'),
            preserve_default=True,
        ),
    ]
