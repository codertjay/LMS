# Generated by Django 3.1.5 on 2021-02-22 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copy_trading', '0004_copytradeinfo_discord_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='copytradeinfo',
            name='account_password',
            field=models.CharField(default='ss', max_length=100),
            preserve_default=False,
        ),
    ]