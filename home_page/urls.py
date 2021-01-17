from django.urls import path

from blog.views import BlogCreateView
from .views import PricingView, TermsAndConditionView, HomePageView,subscribe_view

app_name = 'home'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('create_post/', BlogCreateView.as_view(), name='create_post'),
    path('price/', PricingView.as_view(), name='price'),
    path('terms/', TermsAndConditionView.as_view(), name='terms_and_condition'),
    path('subscribe/', subscribe_view, name='subscribe'),
]
