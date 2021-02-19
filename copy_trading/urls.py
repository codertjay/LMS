from django.urls import path

from .views import CopyTradeFormView, CopyTradingdashboardView

app_name = 'copy_trade'
urlpatterns = [
    path('copy_trade_form/', CopyTradeFormView.as_view(), name='copy_trade_form'),
    path('copy_trade_dashboard/', CopyTradingdashboardView.as_view(), name='copy_trade_dashboard')

]
