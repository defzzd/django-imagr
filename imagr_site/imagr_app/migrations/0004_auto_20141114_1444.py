# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imagr_app', '0003_auto_20141114_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date_published',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='photo',
            name='date_published',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
