from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from courses.models import Course, Lesson
from memberships.models import UserMembership, Membership


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/course_list.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        course = Course.objects.all()
        if query:
            object_list = course.filter(
                Q(slug__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(allowed_memberships__icontains=query)
            ).distinct()
        else:
            object_list = Course.objects.all()
        return object_list


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'


class LessonDetailView(LoginRequiredMixin, View):

    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        user_membership = get_object_or_404(UserMembership, user=request.user)
        user_membership_type = user_membership.membership.membership_type
        course_allowed_mem_types = course.allowed_memberships.all()

        if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
            # if course_allowed_mem_types == user_membership_type:
            context = {
                'object': lesson
            }
            # elif course_allowed_mem_types == 'Free':
            #     context = {
            #         'object': lesson
            #     }
            # elif
        else:
            context = {
                'object': None,

            }
        print('the user lesson ', lesson)
        print('the user membership type', user_membership_type)
        print('the context', context)
        return render(request, 'courses/lesson_detail.html', context)
