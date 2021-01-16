from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
import stripe
from datetime import datetime

# Create your models here.
MembershipType = (
    ('Free', 'Free'),
    ('Professional', 'Professional'),
    ('Enterprise', 'Enterprise'),
)

User = settings.AUTH_USER_MODEL

stripe.api_key = settings.STRIPE_SECRET_KEY


class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(choices=MembershipType, default='Free', max_length=30)
    price = models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type


class UserMembership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.user_membership.user.username

    @property
    def get_created_date(self):
        try:
            subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
            date = datetime.fromtimestamp(subscription.created)
        except:
            date = ''
        return date

    @property
    def get_next_billing_date(self):
        try:
            subscription = stripe.Subscription.retrieve(self.stripe_subscription_id)
            date = datetime.fromtimestamp(subscription.current_period_end)
        except:
            date = ''
        return date


def post_save_user_membership_create(sender, instance, created, *args, **kwargs):
    if created:
        UserMembership.objects.get_or_create(user=instance)
    user_membership, created = UserMembership.objects.get_or_create(user=instance)
    if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
        new_customer_id = stripe.Customer.create(email=instance.email)
        user_membership.stripe_customer_id = new_customer_id['id']
        user_membership.save()


post_save.connect(post_save_user_membership_create, sender=User)
