from django.contrib import admin

from .models import CopyTrading, CopyTradingSubscription

admin.site.register(CopyTrading)
admin.site.register(CopyTradingSubscription)
