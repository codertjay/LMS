from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View


class HomePageView(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'HomePage/index.html')


class TermsAndConditionView(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'HomePage/terms.html')


class PricingView(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'HomePage/pricing.html')

