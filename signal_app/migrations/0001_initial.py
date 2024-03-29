# Generated by Django 3.1.5 on 2021-01-29 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SignalType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signal_choice', models.CharField(choices=[('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Yearly', 'Yearly')], max_length=20)),
                ('discount', models.FloatField()),
                ('price', models.FloatField()),
                ('stripe_plan_id', models.CharField(max_length=40)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSignalSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_subscription_id', models.CharField(max_length=40)),
                ('active', models.BooleanField(default=False)),
                ('signal_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='signal_app.signaltype')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
