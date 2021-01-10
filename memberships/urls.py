from django.urls import path
from .views import (MemberShipSelectView,
                    payment_view,
                    update_transactions,
                    profile_view, cancel_subscription)

app_name = 'memberships'
urlpatterns = [
    path('', MemberShipSelectView.as_view(), name='membership_select'),
    path('payment/', payment_view, name='payment'),
    path('update_transactions/<str:subscription_id>/',
         update_transactions, name='update_transactions'),
    path('profile/', profile_view, name='profile'),
    path('cancel/', cancel_subscription, name='cancel'),
]
