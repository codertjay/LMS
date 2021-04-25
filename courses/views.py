from time import sleep

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic.base import View
from django_hosts.resolvers import reverse as host_reverse

from Learning_platform.settings import VIMEO_AUTHENTICATE
from courses.forms import CourseCreateEditForm, LessonCreateEditForm, LessonEditForm
from courses.models import Course, Lesson
from home_page.mixins import InstructorAndLoginRequiredMixin


def get_course_membership_type(course_allowed_mem_types):
    if course_allowed_mem_types.filter(membership_type='Free').exists():
        membership_type = 'Free'
    elif course_allowed_mem_types.filter(membership_type='Paid').exists():
        membership_type = 'Paid'
    else:
        membership_type = 'Free'
    return membership_type


def check_path_exist(path_exist):
    if not path_exist:
        sleep(15)
        return True


class CourseCreateView(InstructorAndLoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        form = CourseCreateEditForm()
        course = Course.objects.filter(user=self.request.user)
        return render(self.request, 'DashBoard/instructor/instructor-course-create.html',
                      {'form': form, 'course': course})

    def post(self, *args, **kwargs):
        form = CourseCreateEditForm(self.request.POST, self.request.FILES or None)
        form.image = self.request.POST.get('image')
        form.allowed_memberships = self.request.POST.get('allowed_memberships')
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.save()
            form.save_m2m()
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
        instance.save()
        form.save_m2m()
        messages.success(request, 'The form is  valid')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.warning(request, 'The form isn\'t valid')
    context = {'form': form, 'item': instance, 'course': course}
    return render(request, 'DashBoard/instructor/instructor-course-update.html', context)


class CourseDeleteView(InstructorAndLoginRequiredMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('courses:create_course')
    template_name = 'DashBoard/instructor/instructor-course-delete.html'


class LessonCreateView(InstructorAndLoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        form = LessonCreateEditForm()
        course = Course.objects.filter(user=self.request.user)
        return render(self.request, 'DashBoard/instructor/instructor-lesson-add.html', {'form': form, 'course': course})

    def post(self, *args, **kwargs):
        global video_uri
        form = LessonCreateEditForm(self.request.POST, self.request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.save()
            messages.success(self.request, 'Successfully created Lesson')
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            messages.error(self.request, 'invalid form data')
            return redirect('courses:create_lesson')


@login_required
def lesson_update_view(request, slug=None):
    instance = get_object_or_404(Lesson, slug=slug)
    form = LessonEditForm(request.POST or None, request.FILES or None, instance=instance)
    course = Course.objects.filter(user=request.user)
    video_file = request.POST.get('video')
    if video_file:
        video_uri = VIMEO_AUTHENTICATE.replace(video_uri=instance.video_uri, filename=video_file)
        if video_uri:
            instance.video_uri = video_uri
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'The form is  valid')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.warning(request, 'The form isn\'t valid')
    context = {'form': form, 'item': instance, 'course': course}
    return render(request, 'DashBoard/instructor/instructor-lesson-edit.html', context)


class LessonDeleteView(InstructorAndLoginRequiredMixin, DeleteView):
    model = Lesson
    success_url = '/'
    context_object_name = 'lesson'
    template_name = 'DashBoard/instructor/instructor-lesson-delete.html'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()

        print('the delete object', self.object)
        self.object.delete()
        video_uri = self.object.video_uri
        try:
            video_uri = VIMEO_AUTHENTICATE.delete(video_uri)
            print('The video was deleted', video_uri)
        except Exception as a:
            print(a)
        return redirect('courses:create_lesson')
