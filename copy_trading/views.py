from django.shortcuts import render, redirect
# Create your views here.
from django.views.generic.base import View

from .forms import CopyTradeInfoForm


class CopyTradeFormView(View):
    def get(self, request):
        form = CopyTradeInfoForm()
        return render(request, 'HomePage/copy_trade_form/copy_trade_form.html', {'form': form})

    def post(self, request):
        return redirect('home:home')
