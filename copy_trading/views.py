import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.context_processors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic.base import View

from memberships.views import get_user_membership
from users.forms import UserUpdateForm
from .models import CopyTrading, CopyTradingSubscription


class CopyTradingPaymentView(LoginRequiredMixin, View):

    def get(self, request, trade_choice):
        form = UserUpdateForm(request.FILES or None, instance=request.user)
        copy_trade = CopyTrading.objects.filter(copy_trade_choice=trade_choice).first()
        user_copy_trade_sub = CopyTradingSubscription.objects.filter(user=request.user).first()
        if copy_trade:
            print('this is the copy_trade ', copy_trade)
            """In here i am checking if the user have a current copy_trade if he/she has i would redirect
             the him/her to the copy_trade page"""
            if user_copy_trade_sub:
                print('this is the copy_trade sub', user_copy_trade_sub)
                print('this is the copy_trade sub expiring data', user_copy_trade_sub.expiring_date)
                print('this is the copy_trade sub created_date data', user_copy_trade_sub.created_date)
                print('this is the copy_trade sub active', user_copy_trade_sub.active)
                print('this is the date time now', datetime.now())
                if user_copy_trade_sub.expiring_date > datetime.now() and user_copy_trade_sub.active:
                    return redirect(reverse('copy_trade:copy_trade_payment_done', kwargs={
                        'subscription_id': user_copy_trade_sub.stripe_subscription_id,
                        'copy_trade': user_copy_trade_sub.signal_type
                    }))

        else:
            messages.error(request, 'This copy_trade does not exist')
            return redirect('home:home')
        return render(request, 'HomePage/copy_trade/copy_trade.html', {'copy_trade': copy_trade, 'form': form})

    def post(self, request, *args, **kwargs):
        user_membership = get_user_membership(request)
        print('the data ', request.POST)

        copy_trade_val = request.POST['copy_trade']
        # Note : This is where the charges is taking place if the user has no signal
        if copy_trade_val:
            copy_trade = CopyTrading.objects.filter(copy_trade_choice=copy_trade_val).first()
            if copy_trade:
                try:
                    token = request.POST['stripeToken']
                    if token:
                        customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
                        customer.source = token  # 4242424242424242
                        customer.save()
                        # changed plan to price
                        subscription = stripe.Subscription.create(
                            customer=user_membership.stripe_customer_id,
                            items=[{'price': copy_trade.stripe_plan_id}, ])
                        if subscription.id:
                            stripe.Subscription.modify(
                                subscription.id,
                                cancel_at_period_end=True
                            )
                        return redirect(reverse('copy_trade:copy_trade_payment_done', kwargs={
                            'subscription_id': subscription.id, 'copy_trade': copy_trade
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



