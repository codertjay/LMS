from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic.base import View

from courses.forms import CourseCreateEditForm, LessonCreateEditForm
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
        form = LessonCreateEditForm(self.request.POST, self.request.FILES or None)
        form.image = self.request.FILES.get('image')
        form.video = self.request.FILES.get('video')
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
    template_name = 'DashBoard/instructor/instructor-course-delete.html'

    def get_success_url(self):
        return redirect('courses:list')

