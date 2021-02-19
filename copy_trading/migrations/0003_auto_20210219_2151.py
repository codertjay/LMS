# Generated by Django 3.1.5 on 2021-02-19 20:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('copy_trading', '0002_auto_20210219_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='copytradeinfo',
            name='choice_of_symbols',
        ),
        migrations.AddField(
            model_name='copytradeinfo',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 2, 19, 20, 51, 47, 983013, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
