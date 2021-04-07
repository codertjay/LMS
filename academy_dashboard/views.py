from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from courses.models import Course, Lesson
from courses.views import get_course_membership_type
from memberships.models import UserMembership, Membership
from memberships.utils import cancel_user_subscription
from users.models import Profile


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'StudentDashboard/student-courses.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search')
        course = Course.objects.all()
        course_type = self.request.POST.get('course_type')
        if query:
            object_list = course.filter(
                Q(slug__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tag__icontains=query)
            ).distinct()
        elif course_type:
            object_list = course.filter(allowed_memberships__membership_type=course_type)
        else:
            object_list = Course.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['memberships'] = Membership.objects.all()
        return context


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'StudentDashboard/student-course-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = context['object']
        course.view_count += 1
        course.save()
        lesson = course.first_lesson
        user_membership = get_object_or_404(UserMembership, user=self.request.user)
        user_membership_type = user_membership.memberships.all()
        course_allowed_mem_types = course.allowed_memberships.all()
        print('the user membership type', user_membership_type)
        print('the user course_allowed_mem_type', course_allowed_mem_types)
        if user_membership_type in course_allowed_mem_types:
            context['lesson'] = lesson
        return context


class LessonDetailView(LoginRequiredMixin, View):

    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        user_membership = get_object_or_404(UserMembership, user=request.user)
        user_membership_type = user_membership.memberships.all()
        course_allowed_mem_types = course.allowed_memberships.all()
        print('the user membership type', user_membership_type)
        print('the user course_allowed_mem_type', course_allowed_mem_types)
        if user_membership_type in course_allowed_mem_types:
            context = {'lesson': lesson, 'course': course, }
        else:
            context = {'lesson': None, 'course': course, }
        return render(request, 'StudentDashboard/student-course-detail.html', context)
