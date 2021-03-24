from .models import Coupon
from django import forms


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_name',
                  'percent_off',
                  'coupon_type', ]
