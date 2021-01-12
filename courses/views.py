from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import View

from courses.forms import CourseCreateForm
from courses.models import Course, Lesson
from memberships.models import UserMembership, Membership
from users.models import Profile


def get_course_membership_type(course_allowed_mem_types):
    if course_allowed_mem_types.filter(membership_type='Free').exists():
        membership_type = 'Free'
    elif course_allowed_mem_types.filter(membership_type='Professional').exists():
        membership_type = 'Professional'
    elif course_allowed_mem_types.filter(membership_type='Enterprise').exists():
        membership_type = 'Enterprise'
    else:
        membership_type = 'Free'
    return membership_type




class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'DashBoard/student/student-browse-courses.html'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('search')
        course = Course.objects.all()
        if query:
            object_list = course.filter(
                Q(slug__icontains=query) |
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tag__icontains=query)
            ).distinct()
        else:
            object_list = Course.objects.all()
        return object_list


class StudentCourseListView(View):

    def get(self, request):
        course = self.request.user.profile.applied_courses.all()
        context = {
            'StudentCourse': course
        }
        return render(request, 'DashBoard/student/student-my-courses.html', context)

    def post(self, request):
        return redirect('courses:student_course_list')


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    # template_name = 'courses/course_detail.html'
    template_name = 'DashBoard/student/student-view-course.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = context['object']
        lesson = course.first_lesson
        context['lesson'] = lesson
        user_profile_qs = Profile.objects.filter(user=self.request.user)
        if user_profile_qs:
            user_profile = user_profile_qs.first()
            _applied_course_qs = user_profile.applied_courses.filter(id=course.id)
            print('these are the user applied courses', _applied_course_qs)
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
        if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
            context = {'lesson': lesson, 'course': course, }
        elif user_membership_type == 'Enterprise':
            context = {'lesson': lesson, 'course': course, }
        elif membership_type == user_membership_type:
            context = {'lesson': lesson, 'course': course, }
        elif course_allowed_mem_types == 'Free':
            context = {'lesson': lesson, 'course': course, }
        else:
            context = {'lesson': None, 'course': course, }
        print('the user lesson ', lesson)
        print('the user membership type', user_membership_type)
        print('the context', context)
        return render(request, 'DashBoard/student/student-view-course.html', context)


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseCreateForm
    template_name = 'DashBoard/instructor/instructor-dashboard.html'
