from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.views.generic.base import View

from memberships.views import get_user_membership
from .models import SignalType, UserSignal
from users.forms import UserUpdateForm
import stripe


def monthly_signal():
    monthly_signal_qs = SignalType.objects.filter(signal_choice='Monthly')
    if monthly_signal_qs:
        monthly_signal = monthly_signal_qs.first()
    else:
        monthly_signal = None
    return monthly_signal


def quarterly_signal():
    quarterly_signal_qs = SignalType.objects.filter(signal_choice='Quarterly')
    if quarterly_signal_qs:
        quarterly_signal = quarterly_signal_qs.first()
    else:
        quarterly_signal = None
    return quarterly_signal


def yearly_signal():
    yearly_signal_qs = SignalType.objects.filter(signal_choice='Yearly')
    if yearly_signal_qs:
        yearly_signal = yearly_signal_qs.first()
    else:
        yearly_signal = None
    return yearly_signal


def signalDetailView(request, signal_choice, ):
    form = UserUpdateForm(request.FILES or None, instance=request.user)
    signal_qs = SignalType.objects.filter(signal_choice=signal_choice)
    if signal_qs:
        signal = signal_qs.first()
        return render(request, 'HomePage/signal/signal_detail.html', {'signal': signal, 'form': form})
    else:
        messages.error(request, 'This signal does not exist')
        return redirect('home:home')


class SignalPaymentView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        user_membership = get_user_membership(self.request)
        print('the post',self.request.POST)
        if self.request.method == 'POST':
            try:
                token = self.request.POST['stripeToken']
                signal_val = self.request.POST['stripeToken']
                if signal_val:
                    signal_qs = SignalType.objects.filter(signal_choice=signal_val)
                    if signal_qs:
                        signal = signal_qs.first()
                        print('this is the token', token)
                        customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
                        charge = stripe.Charge.create(
                            customer=customer,
                            amount=signal.price,
                            currency='usd',
                            description='Signal payment'
                        )
                        return render(self.request, 'HomePage/signal/signal_payment_done.html', {'signal': signal})
            except Exception as a:
                print('there was an error', a)
        return redirect('home:home')


