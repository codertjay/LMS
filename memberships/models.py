from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
import stripe
from datetime import datetime
from django.db.models import Model
import stripe

# Create your models here.
MembershipType = (
    ('Beginner ', 'Beginner '),
    ('Intermediate ', 'Intermediate '),
    ('Advanced ', 'Advanced '),
)

User = settings.AUTH_USER_MODEL

stripe.api_key = settings.STRIPE_SECRET_KEY


class MembershipManager(models.Manager):
    def get_membership(self, keyword):
        membership = self.filter(slug=keyword).first()
        if membership:
            return membership
        return None


class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(choices=MembershipType, max_length=30, default='Free')
    stripe_plan_id = models.CharField(max_length=40)
    objects = MembershipManager()

    def __str__(self):
        return self.membership_type

    @property
    def price(self):
        try:
            response = stripe.Price.retrieve(self.stripe_plan_id)
            price = response['unit_amount'] / 100
            return price
        except:
            return 0

    @property
    def discount(self):
        try:
            response = stripe.Price.retrieve(self.stripe_plan_id)
            price = response['unit_amount'] / 80
            return price
        except:
            return 0


class UserMembershipsManager(models.Manager):

    def get_user_memberships(self, user):
        user_membership_qs = self.filter(user=user)
        if user_membership_qs.exists():
            user_membership = user_membership_qs.first()
            return user_membership
        return None


class UserMembership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    memberships = models.ManyToManyField(Membership)
    objects = UserMembershipsManager()

    def __str__(self):
        return f"{self.user.username } -- memberships"


def post_save_user_membership_create(sender, instance, created, *args, **kwargs):
    if created:
        UserMembership.objects.get_or_create(user=instance)
    user_membership, created = UserMembership.objects.get_or_create(user=instance)
    if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
        new_customer_id = stripe.Customer.create(email=instance.email)
        user_membership.stripe_customer_id = new_customer_id['id']
        user_membership.save()


post_save.connect(post_save_user_membership_create, sender=User)
