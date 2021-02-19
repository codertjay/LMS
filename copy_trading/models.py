from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model

account_type = (
    ('MT4', 'MT4'),
    ('MT5', 'MT5'),
)
Yes_or_No = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)


class CopyTradeInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=80)
    account_type = models.CharField(choices=account_type,max_length=10)
    account_number = models.CharField(max_length=100)
    broker = models.CharField(max_length=100)
    Broker_server = models.CharField(max_length=100)
    choice_of_symbols = models.CharField(max_length=100)
    slippage = models.CharField(choices=Yes_or_No, max_length=6)
    forex_pairs = models.CharField(choices=Yes_or_No, max_length=6)
    indices = models.CharField(choices=Yes_or_No, max_length=6)
    metals = models.CharField(choices=Yes_or_No, max_length=6)


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
