import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView

from _coupon.models import Coupon
from home_page.models import ComingSoon
from signal_app.models import UserSignalSubscription
from .models import Membership, UserMembership
from .utils import get_user_membership, get_selected_membership, membership_created_message


def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        current_membership = user_membership_qs.first()
        return current_membership
    return None


@login_required
def user_subscriptions_view(request):
    user_membership = UserMembership.objects.get_user_memberships(request.user)
    user_signal_sub = UserSignalSubscription.objects.get_user_signal_sub(
        user=request.user)

    print(user_membership)
    if user_membership:
        user_memberships = user_membership.memberships.all()
    context = {
        'user_membership': user_membership,
        'user_memberships': user_memberships,
        'user_signal_sub': user_signal_sub,
    }
    return render(request, 'DashBoard/payment/student-account-billing-subscription.html', context)


class MemberShipSelectView(LoginRequiredMixin, ListView):
    model = Membership
    template_name = 'DashBoard/payment/student-account-upgrade.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_memberships'] = current_membership.memberships.all()
        return context

    def post(self, request, *args, **kwargs):
        selected_membership_type = request.POST.get('membership_type')
        print('the selected memberships', selected_membership_type)
        user_membership = UserMembership.objects.get_user_memberships(request.user)

        selected_membership_qs = Membership.objects.filter(
            membership_type=selected_membership_type
        )
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()
        """
        ====================================
        VALIDATION 424242424242424
        ===================================
        """
        try:
            if selected_membership in user_membership.memberships.all():
                print('passed this place')
                messages.info(
                    request, 'You already have this selected membership')
                # return HttpResponseRedirect(request.META.get('HTTP_REFER'))
                return redirect('memberships:profile')
        except:
            pass
        # assign to the session
        request.session['selected_membership_type'] = selected_membership.membership_type
        return HttpResponseRedirect(reverse('memberships:payment'))


@login_required
def payment_view(request):
    user_membership = UserMembership.objects.get_user_memberships(request.user)

    selected_membership = get_selected_membership(request)
    publish_key = settings.STRIPE_PUBLISHABLE_KEY
    coming_soon = ComingSoon.objects.first()

    print('passed here 1')

    if coming_soon:
        if coming_soon.coming_soon == True:
            return redirect('home:coming_soon')
    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            coupon = request.POST['coupon']
            customer = stripe.Customer.retrieve(
                user_membership.stripe_customer_id)
            customer.source = token  # 4242424242424242 for testing
            customer.save()
            if coupon:
                coupon_type = Coupon.objects.get_coupon_by_coupon_model(
                    coupon_slug=coupon, subscription_type='Academy')

                if coupon_type:
                    subscription = stripe.Subscription.create(
                        customer=user_membership.stripe_customer_id,
                        items=[
                            {'price': selected_membership.stripe_plan_id},
                        ],
                        coupon=coupon_type.slug,
                    )
            else:
                subscription = stripe.Subscription.create(
                    customer=user_membership.stripe_customer_id,
                    items=[
                        {'price': selected_membership.stripe_plan_id},
                    ]
                )

            print('this is the subscription_id ', subscription.id)
            if subscription.status == 'active':
                print('passed here 2')
                return redirect(reverse('memberships:update_transactions',
                                        kwargs={
                                            'subscription_id': subscription.id
                                        }))
            else:
                messages.warning(
                    request, 'Your payment was incomplete please try using another card')
        except stripe.error.CardError as e:
            messages.info(request, 'Your card has being declined')
        except stripe.error.APIConnectionError as e:
            messages.info(request, 'Network communication with Stripe failed')
        except stripe.error.StripeError as e:
            messages.info(request, 'There was an error we are working on it')
        except Exception as a:
            messages.info(request, 'There error was', a)
            print(f"""
======================================
Error  {a}
======================================
                    """)
    context = {
        'publish_key': publish_key,
        'selected_membership': selected_membership
    }
    return render(request, 'DashBoard/payment/student-pay.html', context)


@login_required
def update_transactions(request, subscription_id):
    print('passed here 3')

    user_membership = UserMembership.objects.get_user_memberships(request.user)
    selected_membership = get_selected_membership(request)
    user_membership.memberships.add(selected_membership)
    user_membership.save()

    # sending message to the user that he has successfully a created membership
    membership_created_message(user_membership, user_membership)
    try:
        del request.session['selected_membership_type']
        messages.info(request, f'Your Payment was successful ')
    except Exception as a:
        print(f"""
======================================
Error  {a}
======================================
                """)
    return redirect('memberships:profile')
