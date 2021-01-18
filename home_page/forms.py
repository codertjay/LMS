from .models import Subscribe

from django import forms
from .models import Testimonial

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = '__all__'
