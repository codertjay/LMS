import stripe
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.datetime_safe import datetime
from django.db.models import Model

from .utils import copy_trading_created_message, copy_trading_expired_message

copy_choices = (
    ('Monthly', 'Monthly'),
)


class CopyTradeManager(models.Manager):
    def copy_trade_filter_choice(self, keyword):
        copy_trade = self.filter(copy_trade_choice=keyword).first()
        if copy_trade:
            return copy_trade
        return None


class CopyTrading(models.Model):
    copy_trade_choice = models.CharField(max_length=20, choices=copy_choices, default='Monthly')
    discount = models.FloatField()
    price = models.FloatField()
    stripe_plan_id = models.CharField(max_length=40)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CopyTradeManager()

    def __str__(self):
        return self.copy_trade_choice


class CopyTradingSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    copy_trade = models.ForeignKey(CopyTrading, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.copy_trade.copy_trade_choice} --{self.user}"

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


# this function deactivate expired copy_trades it sends message to the user whom copy_trades has being deactivated
def deactivate_copy_trading():
    copy_trade_qs = CopyTradingSubscription.objects.all()
    for copy_trade in copy_trade_qs:
        if copy_trade.expiring_date:
            if copy_trade.expiring_date < datetime.now():
                copy_trade.stripe_subscription_id = ''
                copy_trade.active = False
                copy_trading_expired_message(copy_trade)
                copy_trade.save()
    return None


# calling function that deactivate expired copy_trades
deactivate_copy_trading()


# a django copy_trade that automatically send message to the user that has registered on a copy_trade
def post_save_send_user_message_on_copy_trading_subscription(sender, instance, created, *args, **kwargs):
    # send message to the user
    if created:
        print('this is the instance', instance.user)
        copy_trading_created_message(instance)


post_save.connect(post_save_send_user_message_on_copy_trading_subscription, sender=CopyTradingSubscription)
