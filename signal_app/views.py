import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic.base import View

from memberships.views import get_user_membership
from users.forms import UserUpdateForm
from .models import SignalType, UserSignalSubscription


class SignalPaymentView(LoginRequiredMixin, View):

    def get(self, request, signal_choice):
        form = UserUpdateForm(request.FILES or None, instance=request.user)
        signal = SignalType.objects.filter(signal_choice=signal_choice).first()
        user_signal_sub = UserSignalSubscription.objects.filter(user=request.user).first()
        
        if signal:
            print(signal)
            """In here i am checking if the user have a current signal if he/she has i would redirect
             the him/her to the signal page"""
            if user_signal_sub:
                if user_signal_sub.expiring_date:
                    if user_signal_sub.expiring_date > datetime.now() and user_signal_sub.active:
                        return redirect(reverse('signal:signal_payment_done', kwargs={
                            'subscription_id': user_signal_sub.stripe_subscription_id,
                            'signal': user_signal_sub.signal_type
                        }))

        else:
            
            return redirect('home:home')
        return render(request, 'HomePage/signal/signal_detail.html', {'signal': signal, 'form': form})

    def post(self, request, *args, **kwargs):
        user_membership = get_user_membership(request)
        user = User.objects.filter(username=request.user.username).first()
        if user:
            if request.POST['first_name']:
                user.first_name = request.POST['first_name']
            if request.POST['last_name']:
                user.last_name = request.POST['last_name']
            user.save()
        signal_val = request.POST['Signal']
        # Note : This is where the charges is taking place if the user has no signal
        if signal_val:
            signal = SignalType.objects.filter(signal_choice=signal_val).first()
            if signal:
                try:
                    token = request.POST['stripeToken']
                    if token:
                        customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
                        customer.source = token  # 4242424242424242
                        customer.save()
                        # changed plan to price
                        subscription = stripe.Subscription.create(
                            customer=user_membership.stripe_customer_id,
                            items=[{'price': signal.stripe_plan_id}, ])
                        if subscription.id:
                            stripe.Subscription.modify(
                                subscription.id,
                                cancel_at_period_end=True
                            )
                        return redirect(reverse('signal:signal_payment_done', kwargs={
                            'subscription_id': subscription.id, 'signal': signal
                        }))
                except stripe.error.CardError as e:
                    messages.info(request, 'Your card has being declined')
                except stripe.error.APIConnectionError as e:
                    messages.info(request, 'Network communication with Stripe failed')
                except stripe.error.StripeError as e:
                    messages.info(request, 'There was an error we are working on it')
                except Exception as e:
                    messages.info(request, 'There error was', e)
        messages.info(request, 'There was an error ')
        return redirect('home:home')


@login_required
def signal_payment_done(request, subscription_id, signal):
    signal_ = SignalType.objects.filter(signal_choice=signal).first()
    # checking the stripe subscription id if it exists
    # stripe_id = stripe.Charge.retrieve(subscription_id)
    stripe_id = stripe.Subscription.retrieve(subscription_id)
    if signal_ and stripe_id.id == subscription_id:
        if signal_ and stripe_id.id == subscription_id:
            sub, created = UserSignalSubscription.objects.get_or_create(signal_type=signal_, user=request.user)
            if sub.stripe_subscription_id == '' or sub.stripe_subscription_id is None or sub.expiring_date < datetime.now() or sub.active == False:
                sub.stripe_subscription_id = subscription_id
                sub.active = True
                sub.save()
            context = {'signal': signal_}
            return render(request, 'HomePage/signal/signal_payment_done.html', context)

    else:
        messages.error(request, 'There was an error ')
    return redirect('home:home')
