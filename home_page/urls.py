from django.urls import path
from .views import PricingView, TermsAndConditionView, HomePageView

app_name = 'courses'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('price/', PricingView.as_view(), name='price'),
    path('terms/', TermsAndConditionView.as_view(), name='terms_and_condition'),
]
