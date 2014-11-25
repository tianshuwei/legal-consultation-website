# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20141124_1658'),
        ('accounts', '0002_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('publish_date', models.DateTimeField(auto_now=True, verbose_name=b'date published')),
                ('client', models.ForeignKey(to='accounts.Client')),
                ('product', models.ForeignKey(to='products.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question_text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_flag', models.IntegerField(default=0)),
                ('text', models.TextField()),
                ('publish_date', models.DateTimeField(auto_now=True, verbose_name=b'date published')),
                ('question', models.ForeignKey(to='accounts.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='lawyer',
            name='remarks',
        ),
    ]
