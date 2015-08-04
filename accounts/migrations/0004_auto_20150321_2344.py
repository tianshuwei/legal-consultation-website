# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0003_auto_20150308_1859'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('state', models.IntegerField(default=0, choices=[(0, b'NEW'), (1, b'VIEWED')])),
                ('publish_date', models.DateTimeField(auto_now=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='question',
            name='client',
        ),
        migrations.RemoveField(
            model_name='question',
            name='lawyer',
        ),
        migrations.RemoveField(
            model_name='question_text',
            name='question',
        ),
        migrations.DeleteModel(
            name='Question_text',
        ),
        migrations.RemoveField(
            model_name='lawyer',
            name='questions',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.RemoveField(
            model_name='lawyer',
            name='remarks',
        ),
        migrations.AddField(
            model_name='client',
            name='avatar',
            field=models.ImageField(max_length=255, null=True, upload_to=b'avatar.client/'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lawyer',
            name='avatar',
            field=models.ImageField(max_length=255, null=True, upload_to=b'avatar.lawyer/'),
            preserve_default=True,
        ),
    ]
