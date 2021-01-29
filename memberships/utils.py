from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from memberships.models import Membership, Subscription, UserMembership
from memberships.views import get_user_subscription, get_user_membership

EMAIL_HOST_USER = settings.EMAIL_HOST_USER


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
    try:
        membership_type = request.session['selected_membership_type']
        selected_membership_qs = Membership.objects.filter(
            membership_type=membership_type
        )
        if selected_membership_qs.exists():
            return selected_membership_qs.first()
    except Exception as a:
        print('this is  the error', a)
        return None


# send created mail mail to the user
def membership_created_message(user_membership, sub):
    print('this is the user_membership', user_membership.user)
    html_message = render_to_string('EmailTemplates/user_membership_created_message.html',
                                    {'user_membership': user_membership, 'sub': sub, })
    plain_message = strip_tags(html_message)
    print('the signal email', user_membership.user.email)
    user_membership = user_membership.user.email
    # send message to the user and admin
    send_mail(
        f"AssasinFx Membership ( Created ) ",
        plain_message, EMAIL_HOST_USER, recipient_list=[user_membership, EMAIL_HOST_USER]
        , html_message=html_message, fail_silently=True
    )

    return None


# send mail to the user
def membership_expired_message(user_membership, user_sub):
    try:
        html_message = render_to_string('EmailTemplates/user_membership_expired_message.html',
                                        {'user_membership': user_membership, 'user_sub': user_sub, })
        plain_message = strip_tags(html_message)
        # send  message to the user that his user_membership has being created
        user_membership_email = user_membership.user.email
        send_mail(
            f"AssasinFx Membership ( Expired ) ",
            plain_message, EMAIL_HOST_USER
            , recipient_list=[user_membership_email, EMAIL_HOST_USER], html_message=html_message, fail_silently=True
        )
    except Exception as a:
        print('this is  the error', a)
    return None


def cancel_user_subscription(request):
    try:
        user_sub = get_user_subscription(request)
        if user_sub.active == False:
            print("You dont have an active membership")
        elif user_sub.get_next_billing_date < datetime.now() or user_sub.get_next_billing_date == '' or user_sub.get_next_billing_date is None:
            user_sub.active = False
            user_sub.save()
            free_membership = Membership.objects.filter(membership_type='Free').first()
            user_membership = get_user_membership(request)
            user_membership.membership = free_membership
            user_membership.save()
            membership_expired_message(user_membership, user_sub)
        else:
            print('there was an error')
    except Exception as a:
        print('this is  the error', a)
    return None
