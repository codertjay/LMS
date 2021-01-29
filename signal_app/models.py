from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.datetime_safe import datetime

from .utils import signal_created_message, signal_expired_message
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


class UserSignalSubscriptionManager(models.Manager):

    def get_user_signal_sub(self, user):
        user_signal_sub = self.filter(user=user).first()
        if user_signal_sub:
            return user_signal_sub
        else:
            return None


class UserSignalSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    signal_type = models.ForeignKey(SignalType, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    objects = UserSignalSubscriptionManager()

    def __str__(self):
        return f"{self.signal_type.signal_choice} --{self.user}"

    @property
    def created_date(self):
        try:
            subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
            date = datetime.fromtimestamp(subscription.created)
        except:
            date = None
        return date

    @property
    def expiring_date(self):
        try:
            subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
            date = datetime.fromtimestamp(subscription.current_period_end)
        except:
            date = None
        return date


# this function deactivate expired signals it sends message to the user whom signals has being deactivated
def deactivate_signals():
    try:
        signal_qs = UserSignalSubscription.objects.all()
        checking = """
============================= 
checking for expired signals 
============================= 
        """
        print(checking)
        for signal in signal_qs:
            if signal.active:
                print(""" this are the expired signals """, signal.user)
                if signal.expiring_date < datetime.now() or signal.expiring_date is None or signal.expiring_date == '':
                    signal.stripe_subscription_id = ''
                    signal.active = False
                    signal.save()
                    signal_expired_message(signal)
    except Exception as a:
        print(f"""
======================================
Error  {a}
======================================
        """)
    return None


# calling function that deactivate expired signals
deactivate_signals()


# a django signal that automatically send message to the user that has registered on a signal
def post_save_send_user_message_on_signal_subscription(sender, instance, created, *args, **kwargs):
    # send message to the user
    if created:
        print('this is the instance', instance.user)
        instance.save()
        signal_created_message(instance)


post_save.connect(post_save_send_user_message_on_signal_subscription, sender=UserSignalSubscription)
