from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView

from memberships.models import Membership, UserMembership, Subscription


def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        current_membership = user_membership_qs.first().membership.membership_type
        return current_membership
    return None


def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        current_subscription = user_subscription_qs.first()
        return current_subscription
    return None


class MemberShipSelectView(ListView):
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership)
        print(current_membership)
        return context

    def post(self, request, *args, **kwargs):
        selected_membership_type = request.POST.get('membership_type')
        print(selected_membership_type)
        user_membership = get_user_membership(self.request)
        user_subscription = get_user_subscription(self.request)
        selected_membership_qs = Membership.objects.filter(
            membership_type=selected_membership_type
        )
        if selected_membership_type.exists():
            selected_membership = selected_membership_qs.first()
        """
        ====================================
        VALIDATION
        ===================================
        """
        if user_membership.membership == selected_membership:
            if user_subscription != None:
                messages.info(request, 'You already have this selected membership')
    # return HttpResponseRedirect(Http.Meta.Refer)
