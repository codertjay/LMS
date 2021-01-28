from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.base import View

from blog.models import Post
from copy_trading.models import CopyTrading
from courses.models import Course
from home_page.forms import SubscribeForm, TestimonialForm
from home_page.mixins import InstructorAndLoginRequiredMixin
from home_page.models import Testimonial
from memberships.models import Membership


def freeMembership():
    free_qs = Membership.objects.filter(membership_type='Free')
    if free_qs:
        free = free_qs.first()
    else:
        free = None
    return free


def paidMembership():
    enterprise_qs = Membership.objects.filter(membership_type='Paid')
    if enterprise_qs:
        enterprise = enterprise_qs.first()
    else:
        enterprise = None
    return enterprise


def view_404(request, exception):
    return render(request, 'HomePage/errors/404.html', status=404)


def view_403(request, exception):
    return render(request, 'HomePage/errors/403.html', status=403)


def view_400(request, exception):
    return render(request, 'HomePage/errors/400.html', status=400)


def view_500(request):
    return render(request, 'HomePage/errors/500.html', status=500)


class HomePageView(View):

    def get(self, *args, **kwargs):
        Free_course = Course.objects.filter(allowed_memberships=freeMembership())
        Paid_course = Course.objects.filter(allowed_memberships=paidMembership())
        context = {
            'post': Post.objects.all(),
            'testimonial': Testimonial.objects.all(),
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
        messages.success(request, 'You have successfully subscribed')
    return redirect('home:home')


class TestimonialCreateView(InstructorAndLoginRequiredMixin, CreateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'DashBoard/instructor/instructor-testimonial-create.html'
    success_url = reverse_lazy('home:testimonial_create')

    def get_context_data(self, **kwargs):
        context = super(TestimonialCreateView, self).get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.all()
        return context


class TestimonialUpdateView(InstructorAndLoginRequiredMixin, UpdateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'DashBoard/instructor/instructor-testimonial-create.html'
    success_url = reverse_lazy('home:testimonial_create')

    def get_context_data(self, **kwargs):
        context = super(TestimonialUpdateView, self).get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.all()
        return context


class TestimonialDeleteView(InstructorAndLoginRequiredMixin, DeleteView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'DashBoard/instructor/instructor-testimonial-create.html'
    success_url = reverse_lazy('home:testimonial_create')

    def get_context_data(self, **kwargs):
        context = super(TestimonialDeleteView, self).get_context_data(**kwargs)
        context['testimonials'] = Testimonial.objects.all()
        return context
