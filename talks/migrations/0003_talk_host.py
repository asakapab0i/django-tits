# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0002_auto_20140928_0622'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='host',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
