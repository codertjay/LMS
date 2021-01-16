from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.context_processors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.views import View

from courses.models import RecentCourses, Course
from forum.models import ForumQuestion
from memberships.views import get_user_subscription, get_user_membership
from users.forms import ProfileUpdateForm
from users.models import Profile


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


@login_required
def public_profile_view(request, username):
    user_qs = User.objects.filter(username=username)
    if user_qs:
        user = user_qs.first()
        user_forums = ForumQuestion.objects.filter(user=user)
        recent_course_q = RecentCourses.objects.filter(user=user).first()
        recent_course_qs = recent_course_q.courses.all()
        user_course = Course.objects.filter(user=user)
        context = {
            'user': user,
            'user_forums': user_forums,
            'recent_course_qs': recent_course_qs,
            'user_course': user_course,
        }
        return render(request, 'DashBoard/profile/profile-page.html', context)
    messages.info(request, 'This user profile page does not exist')
    return HttpResponseRedirect(request.META.get('HTTP_REFER'))


@login_required
def Update_profile_view(request, username):
    profile_form = ProfileUpdateForm(request.FILES or None, instance=request.user.profile)
    profile = Profile.objects.filter(user=request.user).first()
    context = {
        'profile': profile,
        'profile_form': profile_form,
    }
    return render(request, 'DashBoard/profile/student-account-edit.html')


class UserProfileUpdate(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        profile_form = ProfileUpdateForm(self.request.FILES or None, instance=self.request.user.profile)
        profile = Profile.objects.filter(user=self.request.user).first()
        context = {
            'profile': profile,
            'profile_form': profile_form,
        }
        return render(self.request, 'DashBoard/profile/student-account-edit.html', context)

    def post(self, *args, **kwargs):
        p_form = ProfileUpdateForm(self.request.POST,
                             self.request.FILES,
                             instance=self.request.user.profile)
        if p_form.is_valid():
            p_form.save()
            print('the form was valid')
            messages.success(self.request, f'Your account has been updated')
            return redirect('')
