from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic.base import View

from memberships.views import get_user_membership
from .models import SignalType, UserSignal, SignalSubscription
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


def signalDetailView(request, signal_choice):
    form = UserUpdateForm(request.FILES or None, instance=request.user)
    signal_qs = SignalType.objects.filter(signal_choice=signal_choice)
    if signal_qs:
        signal = signal_qs.first()
        return render(request, 'HomePage/signal/signal_detail.html', {'signal': signal, 'form': form})
    else:
        messages.error(request, 'This signal does not exist')
        return redirect('home:home')


def signal_payment_view(self, request):
    user_membership = get_user_membership(self.request)
    signal_sub_qs = SignalSubscription.objects.filter(user=self.request.user)
    if self.request.method == 'POST':
        token = request.POST['stripeToken']
        signal_val = request.POST['Signal']
        if signal_sub_qs:
            # In here i am checking if the user have a current signal if he has i would redirect
            # the him/her to the signal page
            signal_sub = signal_sub_qs.first()
            if signal_sub:
                return redirect(reverse('signal:signal_payment_done',
                                        kwargs={
                                            'subscription_id': signal_sub.stripe_subscription_id,
                                            'signal': signal_sub.signal_type
                                        }))
            else:
                # Note : This is where the charges is taking place if the user has no signal
                try:
                    if signal_val:
                        signal_qs = SignalType.objects.filter(signal_choice=signal_val)
                        if signal_qs:
                            signal = signal_qs.first()
                            print('this is the token', token)
                            customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
                            customer.source = token  # 4242424242424242
                            customer.save()
                            subscription = stripe.Subscription.create(
                                customer=user_membership.stripe_customer_id,
                                items=[
                                    {'plan': signal.stripe_plan_id},
                                ]
                            )
                            print('this is the subscription id', subscription.id)
                            return redirect(reverse('signal:signal_payment_done',
                                                    kwargs={
                                                        'subscription_id': subscription.id, 'signal': signal
                                                    }))
                except Exception as a:
                    print('there was an error', a)
        return redirect('home:home')


def signal_payment_done(request, subscription_id, signal):
    signal_qs = SignalType.objects.filter(signal_choice=signal.signal_choice)
    if signal_qs:
        signal_ = signal_qs.first()
    if subscription_id and signal_:
        sub, created = SignalSubscription.objects.get_or_create(user=request.user)
        print('this is the subscription id', subscription_id)
        sub.stripe_subscription_id = subscription_id
        sub.active = True
        sub.signal_type = signal_
        if not sub.expiring_date and sub.created_date:
            if signal.signal_choice == 'Monthly':
                sub.expiring_date = timedelta(weeks=4)
                sub.created_date = datetime.now()
            elif signal.signal_choice == 'Quarterly':
                sub.expiring_date = timedelta(weeks=4)
                sub.created_date = datetime.now()
            elif signal.signal_choice == 'Yearly':
                sub.expiring_date = timedelta(weeks=4)
                sub.created_date = datetime.now()
        sub.save()
        return render(request, 'HomePage/signal/signal_payment_done.html')
    else:
        messages.error(request, 'There was an error ')
        return redirect('home:home')
