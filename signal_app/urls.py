from django.urls import path
from .views import signal_payment_view, signalDetailView, signal_payment_done

app_name = 'signal'
urlpatterns = [
    path('<str:signal_choice>/', signalDetailView, name='signal_detail'),
    path('#/<str:subscription_id>/<str:signal>/', signal_payment_done, name='signal_payment_done'),
    path('', signal_payment_view, name='signal_payment'),
]
