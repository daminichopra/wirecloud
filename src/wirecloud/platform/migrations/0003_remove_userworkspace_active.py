# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platform', '0002_auto_20160127_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userworkspace',
            name='active',
        ),
    ]
