# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imagr_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='image_url',
            field=models.CharField(default=b'Photo Not Found', max_length=1024),
            preserve_default=True,
        ),
    ]
