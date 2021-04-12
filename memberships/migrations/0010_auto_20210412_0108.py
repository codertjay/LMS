# Generated by Django 3.1.5 on 2021-04-12 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0009_auto_20210406_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='membership_type',
            field=models.CharField(choices=[('Beginner ', 'Beginner '), ('Intermediate ', 'Intermediate '), ('Advanced ', 'Advanced '), ('Ninja’s US30 Trading Strategy Course', 'Ninja’s US30 Trading Strategy Course')], default='Free', max_length=100),
        ),
    ]