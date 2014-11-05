# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imagr_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagruser',
            name='followers',
            field=models.ManyToManyField(related_name='ImagrUser_followers', to='imagr_app.ImagrUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='imagruser',
            name='following',
            field=models.ManyToManyField(related_name='ImagrUser_following', to='imagr_app.ImagrUser'),
            preserve_default=True,
        ),
    ]
