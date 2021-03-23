from django.urls import path
from .views import SignalPaymentView, signal_payment_done,cancel_signal_subscription

app_name = 'signal'
urlpatterns = [
    path('<str:signal_choice>/', SignalPaymentView.as_view(), name='signal_payment'),
    path('#/<str:subscription_id>/<str:signal>/', signal_payment_done, name='signal_payment_done'),
    path('#/#/#/cancel_signal/', cancel_signal_subscription, name='cancel_signal_subscription'),
]
