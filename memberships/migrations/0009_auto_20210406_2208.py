# Generated by Django 3.1.5 on 2021-04-06 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0008_auto_20210406_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermembership',
            name='membership',
        ),
        migrations.AddField(
            model_name='usermembership',
            name='memberships',
            field=models.ManyToManyField(to='memberships.Membership'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='membership_type',
            field=models.CharField(choices=[('Beginner ', 'Beginner '), ('Intermediate ', 'Intermediate '), ('Advanced ', 'Advanced ')], default='Free', max_length=30),
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]