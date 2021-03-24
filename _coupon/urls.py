from django.urls import path
from .views import CouponView,coupon_create_view

app_name = 'coupon'
urlpatterns = [
    path('', CouponView.as_view(), name='coupon'),
    path('coupon_create/',coupon_create_view,name='coupon_create')
]
