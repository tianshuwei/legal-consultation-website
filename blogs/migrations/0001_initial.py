# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141125_2031'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=256)),
                ('publish_date', models.DateTimeField(auto_now=True, verbose_name=b'date published')),
                ('tags', models.CharField(default=b'', max_length=256)),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=256)),
                ('user', models.ForeignKey(to='accounts.Lawyer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publish_date', models.DateTimeField(auto_now=True, verbose_name=b'date published')),
                ('text', models.TextField()),
                ('article', models.ForeignKey(to='blogs.BlogArticle')),
                ('user', models.ForeignKey(to='accounts.Lawyer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='blogarticle',
            name='category',
            field=models.ForeignKey(to='blogs.BlogCategory'),
            preserve_default=True,
        ),
    ]
