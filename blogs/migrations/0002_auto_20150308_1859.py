# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogarticle',
            name='clicks',
            field=models.IntegerField(default=0, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='tags',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='title',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='name',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogcategory',
            name='state',
            field=models.IntegerField(default=0, choices=[(0, b'PUBLIC'), (1, b'PRIVATE'), (-1, b'SYSTEM')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='publish_date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogsettings',
            name='state',
            field=models.IntegerField(default=0, choices=[(1, b'DISABLE'), (0, b'PUBLIC')]),
            preserve_default=True,
        ),
    ]
