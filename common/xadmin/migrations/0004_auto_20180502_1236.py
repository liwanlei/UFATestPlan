# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xadmin', '0003_auto_20160715_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='content_type',
            field=models.ForeignKey(verbose_name='content type', blank=True, null=True, to='contenttypes.ContentType', to_field=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='log',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, to_field=django.db.models.deletion.CASCADE),
        ),
    ]
