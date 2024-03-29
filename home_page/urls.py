from django.urls import path

from .views import PricingView, TermsAndConditionView, HomePageView, subscribe_view, TestimonialCreateView, \
    TestimonialUpdateView, TestimonialDeleteView, coming_soon

app_name = 'home'
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('terms/', TermsAndConditionView.as_view(), name='terms_and_condition'),
    path('coming_soon/', coming_soon, name='coming_soon'),

    path('subscribe/', subscribe_view, name='subscribe'),
    path('testimonial_create/', TestimonialCreateView.as_view(), name='testimonial_create'),
    path('testimonial/<int:pk>/update/', TestimonialUpdateView.as_view(), name='testimonial_update'),
    path('testimonial/<int:pk>/delete/', TestimonialDeleteView.as_view(), name='testimonial_delete'),

    #  i changed the url to another page
    path('price/', PricingView.as_view(), name='price'),

]
