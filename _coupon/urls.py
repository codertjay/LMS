from django.urls import path
from .views import CouponView, coupon_create_view, validate_coupon

app_name = 'coupon'
urlpatterns = [
    path('', CouponView.as_view(), name='coupon'),
    path('coupon_create/', coupon_create_view, name='coupon_create'),
    path("check_coupon/<str:coupon>/<str:coupon_type>/", validate_coupon, name="validate_coupon")
]
