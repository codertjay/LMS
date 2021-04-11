from django.urls import path

from .views import user_subscriptions_view, MemberShipSelectView, payment_view, update_transactions,cancel_membership

app_name = 'memberships'
urlpatterns = [
    path('', MemberShipSelectView.as_view(), name='membership_select'),
    path('profile/', user_subscriptions_view, name='profile'),
    path('payment/', payment_view, name='payment'),
    path('update_transactions/<str:subscription_id>/',
         update_transactions, name='update_transactions'),
    path('cancel_subscription/<str:slug>/',
         cancel_membership, name='cancel_membership'),
]
