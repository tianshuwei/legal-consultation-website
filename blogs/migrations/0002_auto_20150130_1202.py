# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcategory',
            options={'verbose_name_plural': 'blog categories'},
        ),
        migrations.AddField(
            model_name='blogarticle',
            name='clicks',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogarticle',
            name='modify_date',
            field=models.DateTimeField(auto_now=True, null=True),
            preserve_default=True,
        ),
#        migrations.AddField(
#            model_name='blogcategory',
#            name='state',
#            field=models.IntegerField(default=0),
#            preserve_default=True,
#        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='accounts.Lawyer', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='blogs.BlogCategory', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogarticle',
            name='publish_date',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
