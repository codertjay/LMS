from django.urls import path

from .views import CopyTradeFormView

app_name = 'copy_trade'
urlpatterns = [

    path('copy_trade_form/', CopyTradeFormView.as_view(), name='copy_trade_form')

]
