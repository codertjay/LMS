# Generated by Django 3.1.5 on 2021-02-25 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copy_trading', '0005_copytradeinfo_account_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='copytradeinfo',
            name='risk',
            field=models.CharField(default='a', max_length=100),
            preserve_default=False,
        ),
    ]
