# Generated by Django 3.1.5 on 2021-01-21 18:07

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210119_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=django_quill.fields.QuillField(default='dddd'),
        ),
    ]
