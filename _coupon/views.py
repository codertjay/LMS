from django.shortcuts import redirect, render
from django.views.generic.base import View
from .models import Coupon
from .forms import CouponForm
from django.contrib import messages
import stripe
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from home_page.mixins import InstructorAndLoginRequiredMixin
from django.http import JsonResponse


class CouponView(InstructorAndLoginRequiredMixin, View):

    def get(self, request):
        coupon = Coupon.objects.all()
        context = {
            'coupon': coupon,
            'form': CouponForm()
        }
        return render(request, 'DashBoard/instructor/instructor-coupon.html', context)

    def post(self, request):
        _id = request.POST.get('id')
        if _id:
            _coupon = Coupon.objects.filter(id=_id).first()
            if _coupon:
                try:
                    _coupon.delete()
                    stripe.Coupon.delete(_coupon.slug)
                except:
                    messages.error(
                        request, 'There was an error performing your request')
        return redirect('coupon:coupon')


@login_required()
def coupon_create_view(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = CouponForm(request.POST)
            if form.is_valid:
                form.save()
                messages.success(
                    request, 'Coupon Was Successfully Created  ')
            else:
                messages.info(
                    request, f'{form.errors} ')
    return redirect('coupon:coupon')


def validate_coupon(request, coupon=None, coupon_type=None):
    response = stripe.Coupon.retrieve(coupon)
    print('the response', response.percent_off)
    print('the coupon type', coupon_type)
    percent_off = response.percent_off
    coupon_qs = Coupon.objects.filter(slug=coupon)
    if coupon_qs:
        coupon = coupon_qs.first()
        print('other', coupon.coupon_type)
        if coupon.coupon_type == coupon_type:
            try:
                data = {
                    'percent_off': percent_off
                }
            except:
                data = "error"
            return JsonResponse(data)
        else:
            data = {
                'percent_off': 0
            }
            return JsonResponse(data)
