# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlatContent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('slug', models.SlugField(max_length=255, help_text='The name by which the template author retrieves this content.')),
                ('content', models.TextField()),
                ('site', models.ForeignKey(to='sites.Site', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'flat content',
            },
        ),
        migrations.AlterUniqueTogether(
            name='flatcontent',
            unique_together=set([('slug', 'site')]),
        ),
    ]
