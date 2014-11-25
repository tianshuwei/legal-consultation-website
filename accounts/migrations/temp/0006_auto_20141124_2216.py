# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20141124_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade', models.IntegerField(default=0)),
                ('publish_date', models.DateTimeField(auto_now=True, verbose_name=b'date published')),
                ('client', models.ForeignKey(to='accounts.Client')),
                ('lawyer', models.ForeignKey(to='accounts.Lawyer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='lawyer',
            name='remarks',
            field=models.ManyToManyField(to='accounts.Client', through='accounts.Remark'),
            preserve_default=True,
        ),
    ]
