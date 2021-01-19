from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.base import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from courses.forms import CourseCreateEditForm, LessonCreateEditForm
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
    # template_name = 'courses/course_list.html'
    paginate_by = 10

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
        page = request.GET.get('page', 1)

        paginator = Paginator(course, 10)
        try:
            course = paginator.page(page)
        except PageNotAnInteger:
            course = paginator.page(1)
        except EmptyPage:
            course = paginator.page(paginator.num_pages)
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
        course.view_count += 1
        course.save()
        lesson = course.first_lesson
        user_membership = get_object_or_404(UserMembership, user=self.request.user)
        user_membership_type = user_membership.membership.membership_type
        course_allowed_mem_types = course.allowed_memberships.all()

        membership_type = get_course_membership_type(course_allowed_mem_types)
        if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
            context['lesson'] = lesson
        elif user_membership_type == 'Enterprise':
            context['lesson'] = lesson
        elif user_membership_type == 'Enterprise' and membership_type == 'Professional':
            context['lesson'] = lesson
        elif membership_type == user_membership_type:
            context['lesson'] = lesson
        elif course_allowed_mem_types == 'Free':
            context['lesson'] = lesson
        else:
            context['lesson'] = None
        print('this is the lesson ', context['lesson'])
        print('this is the user_membership_type ', user_membership_type)
        print('this is the ciurse membership_type ', membership_type)
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
        course.view_count += 1
        course.save()

        user_membership = get_object_or_404(UserMembership, user=request.user)
        user_membership_type = user_membership.membership.membership_type
        course_allowed_mem_types = course.allowed_memberships.all()

        membership_type = get_course_membership_type(course_allowed_mem_types)

        if course_allowed_mem_types.filter(membership_type=user_membership_type).exists():
            context = {'lesson': lesson, 'course': course, }
        elif user_membership_type == 'Enterprise':
            context = {'lesson': lesson, 'course': course, }
        elif user_membership_type == 'Enterprise' and membership_type == 'Professional':
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


class CourseCreateView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        form = CourseCreateEditForm()
        course = Course.objects.filter(user=self.request.user)
        return render(self.request, 'DashBoard/instructor/instructor-course-create.html',
                      {'form': form, 'course': course})

    def post(self, *args, **kwargs):
        form = CourseCreateEditForm(self.request.POST, self.request.FILES or None)
        print(self.request.POST)
        print('form:', form.errors)
        form.image = self.request.POST.get('image')
        form.allowed_memberships = self.request.POST.get('allowed_memberships')
        print('these are the allowed membership', form.allowed_memberships)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = self.request.user
            try:
                for x in self.request.POST.get('allowed_memberships'):
                    _membership = Membership.objects.filter(id=x).first()
                    print('this is the membership', _membership)
                    if _membership:
                        instance.allowed_memberships.add(_membership)
            except Exception as a:
                print('there was an error', a)

            instance.save()
            messages.success(self.request, 'course have being created')
            return HttpResponseRedirect(instance.get_absolute_url())

        elif not form.is_valid():
            messages.error(self.request, 'invalid form data')
        return redirect('blog_create')


@login_required
def course_update_view(request, slug=None):
    instance = get_object_or_404(Course, slug=slug)
    form = CourseCreateEditForm(request.POST or None, request.FILES or None, instance=instance)
    course = Course.objects.filter(user=request.user)
    if form.is_valid():
        instance = form.save(commit=False)
        print(instance.slug)

        try:
            for x in request.POST.get('allowed_memberships'):
                _membership = Membership.objects.filter(id=x).first()
                if _membership:
                    print('this is the memebrship', _membership)
                    instance.allowed_memberships.add(_membership)
                    print('the instance allowed memberships', instance.allowed_memberships)
        except Exception as a:
            print('there was an error', a)

        instance.save()
        print('updating the post', request.POST, '\n', instance.user)
        messages.success(request, 'The form is  valid')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.warning(request, 'The form isn\'t valid')
    context = {'form': form, 'item': instance, 'course': course}
    return render(request, 'DashBoard/instructor/instructor-course-update.html', context)


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    success_url = '/'
    template_name = 'DashBoard/instructor/instructor-course-delete.html'


class LessonCreateView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        form = LessonCreateEditForm()
        course = Course.objects.filter(user=self.request.user)
        return render(self.request, 'DashBoard/instructor/instructor-lesson-add.html', {'form': form, 'course': course})

    def post(self, *args, **kwargs):
        form = LessonCreateEditForm(self.request.POST, self.request.FILES or None)
        print(self.request.POST)
        print('form:', form.errors)
        form.image = self.request.POST.get('image')
        form.video = self.request.POST.get('video')

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.save()
            messages.success(self.request, 'Course has being deleted')
            return HttpResponseRedirect(instance.get_absolute_url())

        else:
            messages.error(self.request, 'invalid form data')
            return redirect('courses:create_lesson')


@login_required
def lesson_update_view(request, slug=None):
    instance = get_object_or_404(Lesson, slug=slug)
    form = LessonCreateEditForm(request.POST or None, request.FILES or None, instance=instance)
    course = Course.objects.filter(user=request.user)
    if form.is_valid():
        instance = form.save(commit=False)
        print(instance.slug)
        instance.save()
        print('updating the post', request.POST, '\n', instance.user)
        messages.success(request, 'The form is  valid')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.warning(request, 'The form isn\'t valid')
    context = {'form': form, 'item': instance, 'course': course}
    return render(request, 'DashBoard/instructor/instructor-lesson-edit.html', context)


class LessonDeleteView(LoginRequiredMixin, DeleteView):
    model = Lesson
    success_url = '/'
    context_object_name = 'lesson'
    template_name = 'DashBoard/instructor/instructor-course-delete.html'

    def get_success_url(self):
        return redirect('courses:list')
