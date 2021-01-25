from django.contrib import admin
from .models import SignalType, UserSignalSubscription

# Register your models here.

admin.site.register(SignalType)
admin.site.register(UserSignalSubscription)
