# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogArticle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=255)),
                ('modify_date', models.DateTimeField(auto_now=True, null=True)),
                ('publish_date', models.DateTimeField()),
                ('clicks', models.IntegerField(default=0)),
                ('tags', models.CharField(default=b'', max_length=255)),
                ('text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='accounts.Lawyer', null=True)),
            ],
            options={
                'verbose_name': '\u535a\u5ba2\u6587\u7ae0',
                'verbose_name_plural': '\u535a\u5ba2\u6587\u7ae0',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', unique=True, max_length=255)),
                ('state', models.IntegerField(default=0)),
                ('lawyer', models.ForeignKey(to='accounts.Lawyer')),
            ],
            options={
                'verbose_name': '\u535a\u5ba2\u5206\u7c7b',
                'verbose_name_plural': '\u535a\u5ba2\u5206\u7c7b',
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
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.IntegerField(default=0)),
                ('items_per_page', models.IntegerField(default=15)),
                ('lawyer', models.OneToOneField(to='accounts.Lawyer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='blogarticle',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='blogs.BlogCategory', null=True),
            preserve_default=True,
        ),
    ]
