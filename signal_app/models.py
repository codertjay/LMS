from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.datetime_safe import datetime

from .utils import signal_created_message
import stripe

signal_choices = (
    ('Monthly', 'Monthly'),
    ('Quarterly', 'Quarterly'),
    ('Yearly', 'Yearly'),
)


class SignalType(models.Model):
    signal_choice = models.CharField(max_length=20, choices=signal_choices)
    discount = models.FloatField()
    price = models.FloatField()
    stripe_plan_id = models.CharField(max_length=40)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.signal_choice


class UserSignalSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    signal_type = models.ForeignKey(SignalType, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.signal_type.signal_choice} --{self.user}"

    @property
    def created_date(self):
        try:
            subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
            date = datetime.fromtimestamp(subscription.created)
        except:
            date = ''
        return date

    @property
    def expiring_date(self):
        try:
            subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
            date = datetime.fromtimestamp(subscription.current_period_end)
        except:
            date = ''
        return date


def post_save_send_user_message_on_signal_subscription(sender, instance, created, *args, **kwargs):
    # send message to the user
    if created:
        signal_created_message(instance.signal_type)


post_save.connect(post_save_send_user_message_on_signal_subscription, sender=UserSignalSubscription)
