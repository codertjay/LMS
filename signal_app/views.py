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

from memberships.models import UserMembership
from memberships.utils import get_user_membership
from users.forms import UserUpdateForm
from .models import SignalType, UserSignalSubscription
from _coupon.models import Coupon


class SignalPaymentView(LoginRequiredMixin, View):

    def get(self, request, signal_choice):
        form = UserUpdateForm(request.FILES or None, instance=request.user)
        signal = SignalType.objects.filter(signal_choice=signal_choice).first()
        user_signal_sub = UserSignalSubscription.objects.filter(
            user=request.user).first()

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

        # stripe.PaymentIntent.create(
        #     amount=signal.price * 100,
        #     currency="usd",
        #     payment_method_types=["card"],
        #     customer=UserMembership.objects.get_user_memberships(request.user).stripe_customer_id
        # )
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
            signal = SignalType.objects.filter(
                signal_choice=signal_val).first()
            if signal:
                try:
                    token = request.POST['stripeToken']
                    coupon = request.POST['coupon']
                    if token:
                        customer = stripe.Customer.retrieve(
                            user_membership.stripe_customer_id)
                        customer.source = token  # 4242424242424242
                        customer.save()
                        # changed plan to price
                        subscription =""
                        if coupon:
                            coupon_type = Coupon.objects.get_coupon_by_coupon_model(
                                coupon_slug=coupon,
                                subscription_type='Signal_' + signal_val)
                            print('the coupon type', coupon_type)
                            if coupon_type:
                                subscription = stripe.Subscription.create(
                                    customer=user_membership.stripe_customer_id,
                                    coupon=coupon_type.slug,
                                    items=[{'price': signal.stripe_plan_id}, ])
                                messages.info(request,f'Successfully applied coupon for {coupon_type} ')

                        else:
                            subscription = stripe.Subscription.create(
                                customer=user_membership.stripe_customer_id,
                                items=[{'price': signal.stripe_plan_id}, ])
                        if subscription:
                            if subscription.status == 'active':
                                if subscription.id:
                                    stripe.Subscription.modify(
                                        subscription.id,
                                        cancel_at_period_end=True
                                    )
                                    messages.success(
                                        request, 'Your payment was successful')
                                    return redirect(reverse('signal:signal_payment_done', kwargs={
                                        'subscription_id': subscription.id, 'signal': signal
                                    }))
                            else:
                                messages.warning(
                                    request, 'Your payment was incomplete please try using another card')
                except stripe.error.CardError as e:
                    messages.warning(request, 'Your card has being declined')
                except stripe.error.APIConnectionError as e:
                    messages.warning(
                        request, 'Network communication with Stripe failed')
                except stripe.error.StripeError as e:
                    messages.warning(
                        request, 'There was an error we are working on it')
                except Exception as e:
                    messages.warning(request, 'There is an error the devs are working on it',)
        return redirect('home:home')


@login_required
def signal_payment_done(request, subscription_id, signal):
    signal_ = SignalType.objects.filter(signal_choice=signal).first()
    # checking the stripe subscription id if it exists
    # stripe_id = stripe.Charge.retrieve(subscription_id)
    stripe_id = stripe.Subscription.retrieve(subscription_id)
    check_sub_id = UserSignalSubscription.objects.filter(
        stripe_subscription_id=stripe_id.id)
    if check_sub_id.count() > 1:
        UserSignalSubscription.objects.filter(
            user=request.user).first().delete()
        messages.warning(request, 'You just attempt theft')
        return redirect('home:home')
    if signal_ and stripe_id.id == subscription_id and stripe_id.status == 'active':
        sub, created = UserSignalSubscription.objects.get_or_create(
            signal_type=signal_, user=request.user)
        if sub.stripe_subscription_id == '' or sub.stripe_subscription_id is None or sub.expiring_date < datetime.now() or sub.active == False:
            sub.stripe_subscription_id = subscription_id
            sub.active = True
            sub.save()
        context = {'signal': signal_}
        return render(request, 'HomePage/signal/signal_payment_done.html', context)

    else:
        messages.error(request, 'There was an error ')
    return redirect('home:home')


@login_required
def cancel_signal_subscription(request):
    user_signal_sub = UserSignalSubscription.objects.get_user_signal_sub(
        request.user)
    if user_signal_sub.active == False:
        messages.info(request, "You dont have an active signal")
        return HttpResponseRedirect(request.META.get('HTTP_REFER'))
    try:
        sub = stripe.Subscription.retrieve(
            user_signal_sub.stripe_subscription_id)
        print('the user signal subscription ', user_signal_sub)
        sub.delete()
        user_signal_sub.delete()
        messages.info(request, 'Successfully cancelled signal subscription  ')
    except:
        print('there was an error ')
        messages.info(request, 'There was an error performing your request ')
    return redirect('memberships:profile')


@login_required
def instructor_cancel_signal_subscription(request, username):
    if request.user.is_superuser:
        user = User.objects.filter(username=username).first()
        if user:
            user_signal_sub = UserSignalSubscription.objects.get_user_signal_sub(user=user)
            if user_signal_sub.active == False:
                messages.info(request, "You dont have an active signal")
                return HttpResponseRedirect(request.META.get('HTTP_REFER'))
            try:
                print('the user signal subscription ', user_signal_sub)
                print('the user signal  ', user_signal_sub.stripe_subscription_id)
                sub = stripe.Subscription.retrieve(
                    user_signal_sub.stripe_subscription_id)
                sub.delete()
                user_signal_sub.delete()
                messages.info(request, 'Successfully cancelled signal subscription  ')
            except:
                print('there was an error ')
                messages.info(request, 'There was an error performing your request ')
    return redirect('users:instructor_dashboard')
