from django.urls import path
from .views import SignalPaymentView, signalDetailView

app_name = 'signal'
urlpatterns = [
    path('<str:signal_choice>/', signalDetailView, name='signal_detail'),
    path('', SignalPaymentView.as_view(), name='signal_payment'),
]
