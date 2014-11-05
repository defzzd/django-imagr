# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=140)),
                ('date_uploaded', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('date_published', models.DateField()),
                ('published', models.CharField(default=b'private', max_length=7, choices=[(b'private', b'Private Photo'), (b'shared', b'Shared Photo'), (b'public', b'Public Photo')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImagrUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('our_date_joined_field', models.DateField(auto_now_add=True)),
                ('our_is_active_field', models.BooleanField(default=False)),
                ('followers', models.ManyToManyField(related_name='followers_rel_+', to='imagr_app.ImagrUser')),
                ('following', models.ManyToManyField(related_name='following_rel_+', to='imagr_app.ImagrUser')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=140)),
                ('date_uploaded', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('date_published', models.DateField()),
                ('published', models.CharField(default=b'private', max_length=7, choices=[(b'private', b'Private Photo'), (b'shared', b'Shared Photo'), (b'public', b'Public Photo')])),
                ('user', models.ForeignKey(to='imagr_app.ImagrUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(related_name='Album_cover', to='imagr_app.Photo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='photos',
            field=models.ManyToManyField(related_name='Album_photos', to='imagr_app.Photo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(to='imagr_app.ImagrUser'),
            preserve_default=True,
        ),
    ]
