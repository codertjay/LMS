from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from courses.models import Course, CourseTag, Lesson
from courses.views import get_course_membership_type
from memberships.models import UserMembership
from memberships.utils import cancel_user_subscription
from users.models import Profile


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'StudentDashboard/student-courses.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search')
        course_tag = self.request.GET.get('course_tag')
        course = Course.objects.all()
        if query and not course_tag:
            object_list = course.filter(
                Q(slug__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tag__icontains=query)
            ).distinct()
        elif course_tag:
            object_list = course.filter(
                Q(slug__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=course_tag) |
                Q(tag__icontains=course_tag)
            ).distinct()
        else:
            object_list = Course.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['course_tag'] = CourseTag
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
        user_membership_type = user_membership.membership.membership_type
        course_allowed_mem_types = course.allowed_memberships.all()

        """ checking if user membership has expired  """
        cancel_user_subscription(self.request)

        membership_type = get_course_membership_type(course_allowed_mem_types)
        if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
            context['lesson'] = lesson
        elif user_membership_type == 'Paid':
            context['lesson'] = lesson
        elif course_allowed_mem_types == 'Free':
            context['lesson'] = lesson
        else:
            context['lesson'] = None
        # print('this is the lesson ', context['lesson'])
        # print('this is the user_membership_type ', user_membership_type)
        # print('this is the ciurse membership_type ', membership_type)
        user_profile_qs = Profile.objects.filter(user=self.request.user)
        if user_profile_qs:
            user_profile = user_profile_qs.first()
            _applied_course_qs = user_profile.applied_courses.filter(id=course.id)
            # print('these are the user applied courses', _applied_course_qs)
            if not _applied_course_qs.exists():
                user_profile.applied_courses.add(course)
        return context


class LessonDetailView(LoginRequiredMixin, View):

    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        user_membership = get_object_or_404(UserMembership, user=request.user)
        user_membership_type = user_membership.membership.membership_type
        course_allowed_mem_types = course.allowed_memberships.all()

        membership_type = get_course_membership_type(course_allowed_mem_types)

        """ checking if user membership has expired  """
        cancel_user_subscription(self.request)

        if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
            context = {'lesson': lesson, 'course': course, }
        elif user_membership_type == 'Paid':
            context = {'lesson': lesson, 'course': course, }
        elif course_allowed_mem_types == 'Free':
            context = {'lesson': lesson, 'course': course, }
        else:
            context = {'lesson': None, 'course': course, }
        # print('the user lesson ', lesson)
        # print('the user membership type', user_membership_type)
        # print('the context', context)
        return render(request, 'StudentDashboard/student-course-detail.html', context)
