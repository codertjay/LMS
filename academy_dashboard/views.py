from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.views.generic import ListView, DetailView
# from django.views.generic.base import View
from django.views.generic.base import View

from courses.models import Course, Lesson
from memberships.models import UserMembership, Membership


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'StudentDashboard/student_course/student-courses.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search')
        course = Course.objects.all()
        course_type = self.request.GET.get('course_type')
        if query:
            object_list = course.filter(
                Q(slug__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        elif course_type:
            print('checking here')
            object_list = course.filter(allowed_memberships__membership_type=course_type)
        else:
            object_list = Course.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['memberships'] = Membership.objects.all()
        return context


class StudentCourseTypeView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'StudentDashboard/student_course/student-courses-course-type.html'
    paginate_by = 10
    course_type = None
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search', None)
        course = Course.objects.all()
        course_type = self.kwargs['course_type']
        if course_type:
            print('checking here', course_type)
            object_list = course.filter(allowed_memberships__slug=course_type)
            if query:
                object_list = course.filter(
                    Q(slug__icontains=query) |
                    Q(title__icontains=query) |
                    Q(description__icontains=query)
                ).distinct()
        else:
            messages.info(self.request, 'This url does not exist  ')
            return redirect('/')
        return object_list

    def get_context_data(self, **kwargs):
        context = super(StudentCourseTypeView, self).get_context_data(**kwargs)
        context['memberships'] = Membership.objects.all()
        context['course_type'] = self.kwargs['course_type']
        return context



class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'StudentDashboard/student_course/student-course-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = context['object']
        course.view_count += 1
        course.save()
        lesson = course.first_lesson
        user_membership = get_object_or_404(UserMembership, user=self.request.user)
        user_membership_type = user_membership.memberships.all()
        course_allowed_mem_types = course.allowed_memberships.all()
        for item in course_allowed_mem_types:
            if item in user_membership_type:
                context['lesson'] = lesson
        print('the user membership type', user_membership_type)
        print('the user course_allowed_mem_type', course_allowed_mem_types)
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
        for item in course_allowed_mem_types:
            if item in user_membership_type:
                context = {'lesson': lesson, 'course': course, }
                return render(request, 'StudentDashboard/student_course/student-course-detail.html', context)

        context = {'lesson': None, 'course': course, }
        messages.info(request, 'You dont have access to this course')
        return render(request, 'StudentDashboard/student_course/student-course-detail.html', context)

# @login_required
# def student_course_list_view(request, course_type):
#     course = Course.objects.all().filter(allowed_memberships__slug=course_type)
#     search = request.GET.get('search')
#     context = {
#         'course_type': course_type,
#         'object_list': course,
#         'memberships': Membership.objects.all()
#     }
#     if search:
#         course_qs = course.filter(
#             Q(slug=search) |
#             Q(title=search) |
#             Q(description=search)
#         )
#         context = {
#             'course_type': course_type,
#             'object_list': course_qs,
#             'memberships': Membership.objects.all(),
#         }
#         return render(request, 'StudentDashboard/student-courses-course-type.html', context)
#     return render(request, 'StudentDashboard/student-courses-course-type.html', context)
