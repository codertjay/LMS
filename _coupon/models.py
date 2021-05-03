from django.db import models
import stripe
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
import string
# Create your models here.


CouponChoice = (
    ('Signal_Monthly', 'Signal_Monthly'),
    ('Signal_Quaterly', 'Signal_Quaterly'),
    ('Signal_Yearly', 'Signal_Yearly'),
    ('Academy', 'Academy'),
)


class CouponManager(models.Manager):

    def get_coupon_by_coupon_model(self, coupon_slug, subscription_type,):
        coupon_qs = self.filter(slug=coupon_slug)
        if coupon_qs:
            coupon = coupon_qs.first()
            print('this is the subscription_type', subscription_type)
            print('this is the coupon.coupon_type', coupon.coupon_type)
            if subscription_type == coupon.coupon_type:
                print('Pass first step')
                if coupon.stripe_coupon_name:
                    print('coupon checked', coupon.stripe_coupon_name)
                    return coupon
        return None


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=20)
    percent_off = models.FloatField(default=0.1)
    coupon_type = models.CharField(max_length=20, choices=CouponChoice)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)
    objects = CouponManager()

    def __str__(self):
        return f"{self.coupon_name} -- {self.coupon_type}"

    def stripe_coupon_name(self):
        coupon = stripe.Coupon.retrieve(self.slug)
        return coupon


def create_slug(instance, new_slug=None):
    slug = instance.coupon_names.translate({ord(c): None for c in string.whitespace})
    if new_slug is not None:
        slug = new_slug
    qs = Coupon.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = f'{slug, qs.first().id}'
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_coupon_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
        stripe_slug = create_slug(instance)
        if instance.slug:
            print('sssssssssssss', stripe_slug)
            stripe_coupon = stripe.Coupon.create(
                percent_off=instance.percent_off,
                duration='once',
                id=instance.slug
            )
            instance.name = stripe_coupon.id
            print('this is the instance coupon ', instance.coupon_name)
        instance.save()


pre_save.connect(pre_save_coupon_receiver, sender=Coupon)
