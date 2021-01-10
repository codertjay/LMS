# Generated by Django 3.1.5 on 2021-01-10 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='video_url',
        ),
        migrations.AddField(
            model_name='lesson',
            name='video',
            field=models.FileField(default='a.mp4', upload_to='video'),
            preserve_default=False,
        ),
    ]