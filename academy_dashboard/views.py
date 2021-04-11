from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.views.generic import ListView, DetailView
# from django.views.generic.base import View
from django.views.generic.base import View
from django_hosts.resolvers import reverse as host_reverse

from courses.models import Course, Lesson
from memberships.models import UserMembership, Membership


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'StudentDashboard/student_course/student-courses.html'
    paginate_by = 15

    def get_queryset(self):
        query = self.request.GET.get('search', None)
        course = Course.objects.all()
        course_type = self.request.GET.get('course_type', None)
        course_language = self.request.GET.get('course_language', None)
        if query:
            object_list = course.filter(
                Q(slug__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query)
            ).distinct()
        elif course_type:
            print('checking here')
            object_list = course.filter(allowed_memberships__membership_type=course_type)
        elif course_language:
            print('this is the course language', course_language)
            object_list = course.filter(course_language=course_language)
        else:
            object_list = Course.objects.all()
        return object_list

    def get_context_data(self, **kwargs):
        context = super(CourseListView, self).get_context_data(**kwargs)
        context['memberships'] = Membership.objects.all()
        user_membership = UserMembership.objects.get_user_memberships(self.request.user)
        context['user_membership'] = user_membership.memberships.all()
        return context


class StudentCourseTypeView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'StudentDashboard/student_course/student-courses-course-type.html'
    paginate_by = 15
    course_type = None

    def get_queryset(self):
        query = self.request.GET.get('search', None)
        course = Course.objects.all()
        course_type = self.kwargs['course_type']
        user_membership = get_object_or_404(UserMembership, user=self.request.user)
        course_language = self.request.GET.get('course_language', None)
        check_user = user_membership.memberships.filter(slug=course_type)
        if not check_user:
            messages.info(self.request, 'You dont have access to view this course')
        if course_type:
            print('checking here', course_type)
            object_list = course.filter(allowed_memberships__slug=course_type)
            if query:
                object_list = course.filter(
                    Q(slug__icontains=query) |
                    Q(title__icontains=query) |
                    Q(description__icontains=query)
                ).distinct()
        if course_language:
            print('this is the course language', course_language)
            object_list = course.filter(course_language=course_language)
        else:
            messages.info(self.request, 'This url does not exist  ')
        return object_list

    def get_context_data(self, **kwargs):
        context = super(StudentCourseTypeView, self).get_context_data(**kwargs)
        course_type = self.kwargs['course_type']
        context['memberships'] = Membership.objects.all()
        context['course_type'] = course_type
        user_membership = UserMembership.objects.get_user_memberships(self.request.user)
        context['user_membership'] = user_membership.memberships.all()
        return context

    def get(self, *args, **kwargs):
        course_type = self.kwargs['course_type']
        course_membership = Membership.objects.get_membership(course_type)
        user_membership = UserMembership.objects.get_user_memberships(user=self.request.user)
        if user_membership:
            print('the user membership ', user_membership)
            if course_membership in user_membership.memberships.all():
                return super(StudentCourseTypeView, self).get(*args, **kwargs)
        if course_membership:
            messages.info(self.request,
                          f'You dont have access to view {course_type} courses please select {course_type} and make payment ')
        return redirect(host_reverse('memberships:membership_select', host='www'))


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

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        print('the object ', self.object.allowed_memberships.all())
        course_allowed_memberships = self.object.allowed_memberships.all()
        user_membership = get_object_or_404(UserMembership, user=self.request.user)
        user_membership_type = user_membership.memberships.all()
        context = self.get_context_data(object=self.object)
        if course_allowed_memberships:
            for item in course_allowed_memberships:
                if item in user_membership_type:
                    return self.render_to_response(context)
                elif item not in user_membership_type:
                    messages.info(self.request,
                                  f'You dont have access to view {item.slug} '
                                  f'courses please select {item.slug} and make payment ')
                    return redirect(host_reverse('memberships:membership_select', host='www'))

        return redirect(host_reverse('course_list', host='academy'))


class LessonDetailView(LoginRequiredMixin, View):

    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        user_membership = get_object_or_404(UserMembership, user=request.user)
        user_membership_type = user_membership.memberships.all()
        course_allowed_mem_types = course.allowed_memberships.all()
        for item in course_allowed_mem_types:
            if item in user_membership_type:
                context = {'lesson': lesson, 'course': course, }
                return render(request, 'StudentDashboard/student_course/student-course-detail.html', context)
        messages.info(self.request,
                      f'You dont have access to view {course_allowed_mem_types.first()} '
                      f'courses please select {course_allowed_mem_types.first()} and make payment ')
        return redirect(host_reverse('memberships:membership_select', host='www'))
