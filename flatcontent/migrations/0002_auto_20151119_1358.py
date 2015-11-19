# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import templatefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('flatcontent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flatcontent',
            name='content',
            field=templatefield.fields.TemplateTextField(),
        ),
    ]
