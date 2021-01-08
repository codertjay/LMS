from django.urls import path
from .views import MemberShipSelectView

app_name = 'memberships'
urlpatterns = [
    path('', MemberShipSelectView.as_view(), name='membership_select'),
]

