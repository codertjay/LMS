from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
import stripe

from memberships.models import Membership, UserMembership, Subscription


def profile_view(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)
    context = {
        'user_membership': user_membership,
        'user_subscription': user_subscription
    }
    print('user_membership', user_membership.membership.membership_type)
    print('user_subscription', user_subscription)
    return render(request, 'memberships/profile.html', context)


def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        current_membership = user_membership_qs.first()
        return current_membership
    return None


def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        current_subscription = user_subscription_qs.first()
        return current_subscription
    return None


def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
        membership_type=membership_type
    )
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None


class MemberShipSelectView(ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership.membership_type)
        print(current_membership)
        return context

    def post(self, request, *args, **kwargs):
        selected_membership_type = request.POST.get('membership_type')
        print(selected_membership_type)
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)
        selected_membership_qs = Membership.objects.filter(
            membership_type=selected_membership_type
        )
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()
        """
        ====================================
        VALIDATION
        ===================================
        """
        if user_membership.membership == selected_membership:
            if user_subscription != None:
                messages.info(request, 'You already have this selected membership')
            return HttpResponseRedirect(request.META.get('HTTP_REFER'))
        # assign to the session
        request.session['selected_membership_type'] = selected_membership.membership_type
        return HttpResponseRedirect(reverse('memberships:payment'))


def payment_view(request):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    publish_key = settings.STRIPE_PUBLISHABLE_KEY
    print('The selected', selected_membership)
    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            print('this is the token', token)
            print('this is the user_membership customer id ', user_membership.stripe_customer_id)
            print('this is the strip plan id ', selected_membership.stripe_plan_id)

            customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
            customer.source = token  # 4242424242424242
            customer.save()

            subscription = stripe.Subscription.create(
                customer=user_membership.stripe_customer_id,
                items=[
                    {'plan': selected_membership.stripe_plan_id},
                ]
            )
            print('this is the subscription_id ', subscription.id)
            return redirect(reverse('memberships:update_transactions',
                                    kwargs={
                                        'subscription_id': subscription.id
                                    }))
        except stripe.error.CardError as e:
            messages.info(request, 'Your card has being declined')
            print('Status is: %s' % e.http_status)
            print('Code is: %s' % e.code)
            # param is '' in this case
            print('Param is: %s' % e.param)
            print('Message is: %s' % e.user_message)
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            pass
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            pass
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            pass
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            pass
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            pass
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            messages.info(request, 'There was an error ')
    context = {
        'publish_key': publish_key,
        'selected_membership': selected_membership
    }
    return render(request, 'memberships/membership_payment.html', context)


def update_transactions(request, subscription_id):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    user_membership.membership = selected_membership
    user_membership.save()
    sub, created = Subscription.objects.get_or_create(
        user_membership=user_membership)
    print('this is the subscription id', subscription_id)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()
    try:
        del request.session['selected_membership_type']
    except:
        pass
    messages.info(request, f'Successfully created {selected_membership}')
    return redirect('courses:list')


def cancel_subscription(request):
    user_sub = get_user_subscription(request)
    if user_sub.active == False:
        messages.info(request, "You dont have an active membership")
        return HttpResponseRedirect(request.META.get('HTTP_REFER'))

    sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
    sub.delete()
    user_sub.active = False
    user_sub.save()
    free_membership = Membership.objects.filter(membership_type='Free').first()
    user_membership = get_user_membership(request)
    user_membership.membership = free_membership
    user_membership.save()
    #Todo: send email to the user
    messages.info(request, 'Successfully cancelled membership. We have sent an email ')
    return redirect('memberships:membership_select')
