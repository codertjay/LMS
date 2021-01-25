from django.urls import path
from .views import CopyTradingPaymentView, copy_trade_payment_done

app_name = 'copy_trade'
urlpatterns = [
    path('<str:copy_trade_choice>/', CopyTradingPaymentView.as_view(), name='copy_trade_payment'),
    path('#/<str:subscription_id>/<str:copy_trade>/', copy_trade_payment_done, name='copy_trade_payment_done'),
]
