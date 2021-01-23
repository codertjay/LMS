from django.contrib import admin
from .models import SignalType, UserSignal

# Register your models here.

admin.site.register(SignalType)
admin.site.register(UserSignal)
