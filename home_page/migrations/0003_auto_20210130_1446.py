# Generated by Django 3.1.5 on 2021-01-30 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0002_auto_20210129_1548'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testimonial',
            old_name='title',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='testimonial',
            name='user',
        ),
    ]
