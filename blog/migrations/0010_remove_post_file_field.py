# Generated by Django 3.0.3 on 2020-05-30 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20200530_2222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='file_field',
        ),
    ]