from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
# Create your views here.
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags
from django.views import View

from academy_forum.models import ForumQuestion
from courses.models import RecentCourses, Course
from home_page.mixins import InstructorAndLoginRequiredMixin
from home_page.models import Subscribe
from memberships.utils import get_user_membership
from signal_app.models import UserSignalSubscription, deactivate_signals
from users.forms import ProfileUpdateForm, ContactAdminForm, UserUpdateForm, SendMailForm
from users.models import Profile, Contact

EMAIL_HOST_USER = settings.EMAIL_HOST_USER_SENDGRID


class StudentDashBoardView(LoginRequiredMixin, View):

    def get(self, request):
        recent_course_qs = RecentCourses.objects.filter(user=request.user)
        user_membership = get_user_membership(request)
        # user_subscription = get_user_subscription(request)
        forum_question = ForumQuestion.objects.filter(user=request.user)
        if recent_course_qs:
            recent_course = recent_course_qs.first()
        else:
            recent_course = None

        context = {
            'active': True,
            'RecentCourse': recent_course,
            'user_membership': user_membership,
            # 'user_subscription': user_subscription,
            'forum_requestion': forum_question,
        }
        return render(request, 'DashBoard/student/student-dashboard.html', context)

    def post(self, request):
        return redirect('dashboard:student_dashboard')


class InstructorDashBoardView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.profile.user_type == 'Instructor':
            course_qs = Course.objects.filter(user=request.user)
            signals = UserSignalSubscription.objects.all()
            deactivate_signals()
            try:
                most_viewed_qs = Course.objects.all().order_by('-view_count')
                if most_viewed_qs:
                    most_viewed = most_viewed_qs
                else:
                    most_viewed = None
            except Exception as a:
                most_viewed = None
                print('the error', a)
            if course_qs:
                course = course_qs
            else:
                course = None
            context = {
                'active': True,
                'course': course,
                'most_viewed': most_viewed,
                'signals': signals,
            }
            print('these are the most viewed course', most_viewed)
            return render(request, 'DashBoard/instructor/instructor-dashboard.html', context)
        return redirect('users:profile', request.user.username)

    def post(self, request):
        return redirect('dashboard:instructor_dashboard')


def contactAdminView(request):
    form = ContactAdminForm(request.POST)
    contact = Contact(
        contact_name=form['contact_name'].value(),
        contact_email=form['contact_email'].value(),
        contact_subject=form['contact_subject'].value(),
        contact_message=form['contact_message'].value()
    )
    if form.is_valid():
        contact.save()
        template = get_template('EmailTemplates/contact_admin.txt')
        context = {
            'contact_name': contact.contact_name,
            'contact_email': contact.contact_email,
            'contact_subject': contact.contact_subject,
            'contact_message': contact.contact_message
        }
        content = template.render(context)
        if context:
            send_mail(
                contact.contact_subject,
                content,
                contact.contact_email,
                [EMAIL_HOST_USER],
                fail_silently=True,
            )
            messages.success(request, 'Your message has being sent we would be in touch with you later ')
            return redirect('home:subscribe')
    print('there was an error sending your message')
    messages.warning(request, 'There was an error please try again later ')
    return redirect('home:home')


@login_required
def public_profile_view(request, username):
    user_qs = User.objects.filter(username=username).first()

    if user_qs:
        user = user_qs
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
        return render(request, 'public-profile.html', context)
    else:
        messages.info(request, f"{user_qs}")
        return redirect("memberships:profile")


class UserProfileUpdate(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        user_form = UserUpdateForm(instance=self.request.user, )
        profile_form = ProfileUpdateForm(self.request.FILES or None, instance=self.request.user.profile)
        profile = Profile.objects.filter(user=self.request.user).first()
        context = {
            'profile': profile,
            'profile_form': profile_form,
            'user_form': user_form,
        }
        return render(self.request, 'DashBoard/profile/student-account-edit.html', context)

    def post(self, *args, **kwargs):
        p_form = ProfileUpdateForm(self.request.POST,
                                   self.request.FILES or None,
                                   instance=self.request.user.profile)
        u_form = UserUpdateForm(self.request.POST, instance=self.request.user)
        profile_pics = self.request.FILES.get('profile_pics')
        background_image = self.request.FILES.get('background_image')
        print(profile_pics, background_image)
        if u_form.is_valid() and p_form.is_valid():
            username = u_form.cleaned_data.get('username')
            email = u_form.cleaned_data.get('email')
            first_name = u_form.cleaned_data.get('first_name')
            last_name = u_form.cleaned_data.get('last_name')
            u_form.save()
            profile_form = p_form.save(commit=False)
            if profile_pics:
                profile_form.profile_pics = self.request.FILES.get('profile_pics')
            if background_image:
                profile_form.background_image = self.request.FILES.get('background_image')
            profile_form.save()
            print('the form was valid')
            messages.success(self.request, f'Your account has been updated')
        else:
            messages.warning(self.request, f'There was an error please filled the form correctly')
        return redirect('users:profile_edit')


# send created mail mail to the user
def instructor_send_message(message, email_list):
    html_message = render_to_string('EmailTemplates/instructor_send_message_template.html',
                                    {'content': message.get('content'), 'title': message.get('title')})
    plain_message = strip_tags(html_message)
    send_mail(
        f"{message.get('title')}",
        plain_message, EMAIL_HOST_USER, recipient_list=email_list
        , html_message=html_message, fail_silently=True
    )
    return None


class InstructorSendMail(InstructorAndLoginRequiredMixin, View):

    def get(self, request):
        form = SendMailForm()
        context = {'form': form}
        return render(self.request, 'DashBoard/instructor/instructor-sendmail.html', context)

    def post(self, request):
        email_list = EmailAddress.objects.all()
        print('the post', self.request.POST)
        form = SendMailForm(request.POST)
        email_list = []
        for item in EmailAddress.objects.all():
            email_list.append(item.email)
        for item in Subscribe.objects.all():
            email_list.append(item.email)
        print('the email list', email_list)
        list_of_emails = list(dict.fromkeys(email_list))
        if form.is_valid():
            print('the form content', form.cleaned_data)
            message = form.cleaned_data
            instructor_send_message(message, list_of_emails)
            messages.success(request, 'Successfully sent message')
        return redirect('users:send_mail')
