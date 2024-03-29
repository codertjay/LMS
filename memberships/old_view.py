# from datetime import datetime
#
# import stripe
# from django.conf import settings
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.http import HttpResponseRedirect
# from django.shortcuts import render, redirect
# from django.urls import reverse
# from django.views.generic import ListView
#
# from courses.models import RecentCourses
# from memberships.models import Membership, Subscription
# from memberships.utils import get_user_membership, get_user_subscription, get_selected_membership, \
#     membership_created_message
# from signal_app.models import UserSignalSubscription
# from home_page.models import ComingSoon
# from _coupon.models import Coupon
#
#
# @login_required
# def user_subscriptions_view(request):
#     user_membership = get_user_membership(request)
#     user_subscription = get_user_subscription(request)
#     user_signal_sub = UserSignalSubscription.objects.get_user_signal_sub(
#         user=request.user)
#     context = {
#         'user_membership': user_membership,
#         'user_subscription': user_subscription,
#         'membership_type': user_membership.membership.membership_type,
#         'membership_price': user_membership.membership.price,
#         'user_signal_sub': user_signal_sub,
#     }
#     return render(request, 'DashBoard/payment/student-account-billing-subscription.html', context)
#
#
# class MemberShipSelectView(LoginRequiredMixin, ListView):
#     model = Membership
#     template_name = 'DashBoard/payment/student-account-upgrade.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         current_membership = get_user_membership(self.request)
#         context['current_membership'] = str(
#             current_membership.membership.membership_type)
#         return context
#
#     def post(self, request, *args, **kwargs):
#         selected_membership_type = request.POST.get('membership_type')
#         print(selected_membership_type)
#
#         user_membership = get_user_membership(request)
#         user_subscription = get_user_subscription(request)
#         selected_membership_qs = Membership.objects.filter(
#             membership_type=selected_membership_type
#         )
#         if selected_membership_qs.exists():
#             selected_membership = selected_membership_qs.first()
#         """
#         ====================================
#         VALIDATION
#         ===================================
#         """
#         try:
#             print('this is gthe user subscription', user_subscription.get_next_billing_date)
#             if user_subscription:
#                 print('this is gthe user subscription',user_subscription)
#                 if user_subscription.get_next_billing_date > datetime.now():
#                     if user_membership.membership == selected_membership:
#                         if user_subscription != None:
#                             messages.info(
#                                 request, 'You already have this selected membership')
#                         return HttpResponseRedirect(request.META.get('HTTP_REFER'))
#                     elif user_membership.membership.membership_type == 'Advanced' and user_subscription != None:
#                         messages.info(
#                             request, 'You already have access to Advanced membership')
#                         return HttpResponseRedirect(request.META.get('HTTP_REFER'))
#         except:
#             pass
#         # assign to the session
#         request.session['selected_membership_type'] = selected_membership.membership_type
#         return HttpResponseRedirect(reverse('memberships:payment'))
#
#
# @login_required
# def payment_view(request):
#     user_membership = get_user_membership(request)
#     selected_membership = get_selected_membership(request)
#     publish_key = settings.STRIPE_PUBLISHABLE_KEY
#     coming_soon = ComingSoon.objects.first()
#
#     print('the user membership',user_membership.membership)
#     print('the selected_membership ',selected_membership)
#
#
#     if coming_soon:
#         if coming_soon.coming_soon == True:
#             return redirect('home:coming_soon')
#     if request.method == 'POST':
#         try:
#             token = request.POST['stripeToken']
#             coupon = request.POST['coupon']
#             customer = stripe.Customer.retrieve(
#                 user_membership.stripe_customer_id)
#             customer.source = token  # 4242424242424242 for testing
#             customer.save()
#             if coupon:
#                 coupon_type = Coupon.objects.get_coupon_by_coupon_model(
#                     coupon_slug=coupon, subscription_type='Academy')
#
#                 if coupon_type:
#                     subscription = stripe.Subscription.create(
#                         customer=user_membership.stripe_customer_id,
#                         items=[
#                             {'price': selected_membership.stripe_plan_id},
#                         ],
#                         coupon=coupon_type.slug,
#                     )
#             else:
#                 subscription = stripe.Subscription.create(
#                     customer=user_membership.stripe_customer_id,
#                     items=[
#                         {'price': selected_membership.stripe_plan_id},
#                     ]
#                 )
#
#             print('this is the subscription_id ', subscription.id)
#             if subscription.status == 'active':
#                 return redirect(reverse('memberships:update_transactions',
#                                         kwargs={
#                                             'subscription_id': subscription.id
#                                         }))
#             else:
#                 messages.warning(
#                     request, 'Your payment was incomplete please try using another card')
#         except stripe.error.CardError as e:
#             messages.info(request, 'Your card has being declined')
#         except stripe.error.APIConnectionError as e:
#             messages.info(request, 'Network communication with Stripe failed')
#         except stripe.error.StripeError as e:
#             messages.info(request, 'There was an error we are working on it')
#         except Exception as a:
#             messages.info(request, 'There error was', a)
#             print(f"""
# ======================================
# Error  {a}
# ======================================
#                     """)
#     context = {
#         'publish_key': publish_key,
#         'selected_membership': selected_membership
#     }
#     return render(request, 'DashBoard/payment/student-pay.html', context)
#
#
# @login_required
# def update_transactions(request, subscription_id):
#     user_membership = get_user_membership(request)
#     selected_membership = get_selected_membership(request)
#     user_membership.membership = selected_membership
#     user_membership.save()
#     sub, created = Subscription.objects.get_or_create(
#         user_membership=user_membership)
#     # print('this is the subscription id', subscription_id)
#     sub.stripe_subscription_id = subscription_id
#     sub.active = True
#     sub.save()
#     # sending message to the user that he has successfully a created membership
#     membership_created_message(user_membership, sub)
#     try:
#         del request.session['selected_membership_type']
#         messages.info(request, f'Your Payment was successful ')
#     except Exception as a:
#         print(f"""
# ======================================
# Error  {a}
# ======================================
#                 """)
#     return redirect('memberships:profile')
#
#
# @login_required
# def cancel_subscription(request):
#     user_sub = get_user_subscription(request)
#     if user_sub.active == False:
#         messages.info(request, "You dont have an active membership")
#         return HttpResponseRedirect(request.META.get('HTTP_REFER'))
#     try:
#         sub = stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
#         sub.delete()
#         user_sub.active = False
#         user_sub.save()
#     except:
#         messages.info(request, 'There was an error performing your request ')
#
#     free_membership = Membership.objects.filter(membership_type='Free').first()
#     user_membership = get_user_membership(request)
#     user_membership.membership = free_membership
#     user_membership.save()
#     messages.info(
#         request, 'Successfully cancelled Academy  subscription. ')
#     return redirect('memberships:membership_select')
#
#
# @login_required
# def student_membership_invoice(request):
#     user_membership = get_user_membership(request)
#     user_subscription = get_user_subscription(request)
#
#     recent_course_qs = RecentCourses.objects.filter(user=request.user)
#     user_membership = get_user_membership(request)
#     user_subscription = get_user_subscription(request)
#
#     if recent_course_qs:
#         recent_course = recent_course_qs.first()
#     else:
#         recent_course = None
#     if user_subscription:
#         context = {
#             'user_membership': user_membership,
#             'user_subscription': user_subscription,
#             'membership_type': user_membership.membership.membership_type,
#             'membership_price': user_membership.membership.price,
#             'next_billing_date': user_subscription.get_next_billing_date,
#             'created_at': user_subscription.get_created_date,
#             'recent_course': recent_course,
#         }
#     else:
#         context = {
#             'user_membership': user_membership,
#             'user_subscription': user_subscription,
#             'membership_type': user_membership.membership.membership_type,
#             'membership_price': user_membership.membership.price,
#             'recent_course': recent_course,
#         }
#     return render(request, 'DashBoard/payment/student-invoice.html', context)
