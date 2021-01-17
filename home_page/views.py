from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View

from blog.models import Post
from courses.models import Course
from home_page.forms import SubscribeForm
from memberships.models import Membership


def freeMembership():
    free_qs = Membership.objects.filter(membership_type='Free')
    if free_qs:
        free = free_qs.first()
    else:
        free = None
    return free


def professionalMembership():
    professional_qs = Membership.objects.filter(membership_type='Professional')
    if professional_qs:
        professional = professional_qs.first()
    else:
        professional = None
    return professional


def enterpriseMembership():
    enterprise_qs = Membership.objects.filter(membership_type='Enterprise')
    if enterprise_qs:
        enterprise = enterprise_qs.first()
    else:
        enterprise = None
    return enterprise


class HomePageView(View):

    def get(self, *args, **kwargs):
        Free_course = Course.objects.filter(allowed_memberships=freeMembership())
        Professional_course = Course.objects.filter(allowed_memberships=professionalMembership())
        Enterprise_course = Course.objects.filter(allowed_memberships=enterpriseMembership())
        print('the free', Free_course)
        print('the Professional_course', Professional_course)
        print('the Enterpreneur_course', Enterprise_course)
        if Post.objects.count() >= 4:
            post = Post.objects.all()[4]
        elif Post.objects.count() >= 3:
            post = Post.objects.all()[2]
        elif Post.objects.count() >= 2:
            post = Post.objects.all()[2]
        elif Post.objects.count() >= 1:
            post = Post.objects.all()[1]
        else:
            post = None
        context = {
            'post': post,
            'Free_course': Free_course.count(),
            'Free_price': freeMembership().price,
            'Free_discount_price': freeMembership().discount,

            'Professional_course': Professional_course.count(),
            'Professional_price': professionalMembership().price,
            'Professional_discount_price': professionalMembership().discount,

            'Enterprise_course': Enterprise_course.count(),
            'Enterprise_price': enterpriseMembership().price,
            'Enterprise_discount_price': enterpriseMembership().discount,
        }
        return render(self.request, 'HomePage/index.html', context)


class TermsAndConditionView(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'HomePage/terms.html')


class PricingView(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'HomePage/pricing.html')


def subscribe_view(request):
    form = SubscribeForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('home:subscribe_page')
    return redirect('home:home')
