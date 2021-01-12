from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from courses.models import RecentCourses, Course, CourseMessages
from memberships.views import get_user_subscription, get_user_membership


class StudentDashBoardView(LoginRequiredMixin, View):

    def get(self, request):
        recent_course_qs = RecentCourses.objects.filter(user=request.user)
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)

        if recent_course_qs:
            recent_course = recent_course_qs.first()
        else:
            recent_course = None

        print('user_membership', user_membership.membership.membership_type)
        print('user_subscription', user_subscription)
        context = {
            'active': True,
            'RecentCourse': recent_course,
            'user_membership': user_membership,
            'user_subscription': user_subscription
        }
        return render(request, 'DashBoard/student/student-dashboard.html', context)

    def post(self, request):
        return redirect('dashboard:student_dashboard')


class InstructorDashBoardView(LoginRequiredMixin, View):

    def get(self, request):

        context = {
            'active': True
        }
        return render(request, 'DashBoard/instructor/instructor-dashboard.html', context)

    def post(self, request):
        return redirect('dashboard:instructor_dashboard')
