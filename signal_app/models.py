from django.db import models
from django.contrib.auth.models import User

signal_choices = (
    ('Monthly', 'Monthly'),
    ('Quarterly', 'Quarterly'),
    ('Yearly', 'Yearly'),
)


class SignalType(models.Model):
    signal_choice = models.CharField(max_length=20, choices=signal_choices)
    discount = models.FloatField()
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.signal_choice


class UserSignal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    signal_type = models.ForeignKey(SignalType, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.signal_type.signal_choice} --{self.user}"
