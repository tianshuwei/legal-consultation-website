# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20141125_2031'),
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogarticle',
            name='author',
            field=models.ForeignKey(default=None, to='accounts.Lawyer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
