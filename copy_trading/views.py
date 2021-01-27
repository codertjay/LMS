import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views.generic.base import View

from memberships.views import get_user_membership
from users.forms import UserUpdateForm
from .models import CopyTrading, CopyTradingSubscription


class CopyTradingPaymentView(LoginRequiredMixin, View):

    def get(self, request, copy_trade_choice):
        form = UserUpdateForm(request.FILES or None, instance=request.user)
        copy_trade = CopyTrading.objects.filter(copy_trade_choice=copy_trade_choice).first()
        user_copy_trade_sub = CopyTradingSubscription.objects.filter(user=request.user).first()
        if copy_trade:
            """In here i am checking if the user have a current copy_trade if he/she has i would redirect
             the him/her to the copy_trade page"""
            if user_copy_trade_sub:
                if user_copy_trade_sub.expiring_date:
                    if user_copy_trade_sub.expiring_date > datetime.now():
                        return redirect(reverse('copy_trade:copy_trade_payment_done', kwargs={
                            'subscription_id': user_copy_trade_sub.stripe_subscription_id,
                            'copy_trade': user_copy_trade_sub.copy_trade
                        }))

        else:
            messages.error(request, 'This copy_trade does not exist')
            return redirect('home:home')
        return render(request, 'HomePage/copy_trade/copy_trade.html', {'copy_trade': copy_trade, 'form': form})

    def post(self, request, *args, **kwargs):
        user_membership = get_user_membership(request)
        user = User.objects.filter(username=request.user.username).first()
        if user:
            if request.POST['first_name']:
                user.first_name = request.POST['first_name']
            if request.POST['last_name']:
                user.last_name = request.POST['last_name']
            user.save()

        copy_trade_val = request.POST['copy_trade']
        # Note : This is where the charges is taking place if the user has no copy trade
        if copy_trade_val:
            copy_trade = CopyTrading.objects.copy_trade_filter_choice(copy_trade_val)
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
                    messages.error(request, 'Your card has being declined')
                except stripe.error.APIConnectionError as e:
                    messages.error(request, 'Network communication with Stripe failed')
                except stripe.error.StripeError as e:
                    messages.error(request, 'There was an error we are working on it')
                except Exception as e:
                    messages.error(request, 'There error was', e)
        messages.info(request, 'There was an error ')
        return redirect('home:home')


@login_required
def copy_trade_payment_done(request, subscription_id, copy_trade):
    copy_trade_ = CopyTrading.objects.filter(copy_trade_choice=copy_trade).first()
    # checking the stripe subscription id if it exists
    # stripe_id = stripe.Charge.retrieve(subscription_id)
    stripe_id = stripe.Subscription.retrieve(subscription_id)
    if copy_trade_:
        if stripe_id.id == subscription_id:
            sub, created = CopyTradingSubscription.objects.get_or_create(copy_trade=copy_trade_, user=request.user)
            if sub.stripe_subscription_id == '' or sub.stripe_subscription_id is None or sub.expiring_date < datetime.now():
                sub.stripe_subscription_id = subscription_id
                sub.active = True
                sub.save()
            context = {'copy_trade': copy_trade_}
            return render(request, 'HomePage/copy_trade/copy_trade_payment_done.html', context)
    else:
        messages.error(request, 'There was an error ')
    return redirect('home:home')
