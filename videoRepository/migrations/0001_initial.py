# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'Title')),
                ('version', models.CharField(max_length=32, verbose_name=b'Version')),
                ('releaseDate', models.DateField(verbose_name=b'Release Date')),
                ('contentType', models.CharField(max_length=32, verbose_name=b'Content Type')),
                ('language', models.CharField(max_length=32, verbose_name=b'Language')),
                ('barCode', models.BigIntegerField(verbose_name=b'Bar Code')),
                ('md5', models.CharField(max_length=32, verbose_name=b'md5')),
                ('fileName', models.CharField(max_length=200, verbose_name=b'File Name')),
                ('filePath', models.CharField(unique=True, max_length=200, verbose_name=b'File Path')),
                ('person', models.ForeignKey(to='videoRepository.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
