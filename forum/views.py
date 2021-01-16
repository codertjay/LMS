from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from django.views.generic import ListView, DeleteView, DetailView
from django.views.generic.base import View

from .forms import ForumAnswerForm, ForumQuestionForm
from .models import ForumQuestion


class ForumListView(LoginRequiredMixin, ListView):
    model = ForumQuestion
    template_name = 'DashBoard/forum/student-forum.html'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('search')
        course = ForumQuestion.objects.all()
        if query:
            object_list = course.filter(
                Q(user__icontains=query) |
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        else:
            object_list = ForumQuestion.objects.all()
        return object_list


class ForumQuestionCreateView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        form = ForumQuestionForm()
        forum = ForumQuestion.objects.all()
        return render(self.request, 'DashBoard/forum/student-forum-ask.html', {'form': form, 'forum': forum})

    def post(self, *args, **kwargs):
        form = ForumQuestionForm(self.request.POST)
        print(self.request.POST)
        print('form:', form.errors)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.save()
            messages.success(self.request, 'blog post have being created')
            return HttpResponseRedirect(instance.get_absolute_url())

        elif not form.is_valid():
            messages.error(self.request, 'invalid form data')
        return redirect('for')


class ForumQuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = ForumQuestion
    success_url = '/'
    template_name = 'DashBoard/instructor/instructor-course-delete.html'


class ForumQuestionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'DashBoard/forum/student-forum-detail.html'
    model = ForumQuestion
    context_object_name = 'forum_question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = context['object']
        forumquestion_list = ForumQuestion.objects.all()
        context['form'] = ForumAnswerForm()
        context['forumquestion_list'] = forumquestion_list
        return context


@login_required
def forum_answer_create_view(request, pk=None):
    try:
        instance = ForumQuestion.objects.get(pk=pk)
    except ObjectDoesNotExist:
        instance = None
    if request.method == 'POST':
        form = ForumAnswerForm(request.POST)
        print('The form data :', form)
        if form.is_valid():
            print(form.cleaned_data)
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.forum_question = instance
            form.save()
            messages.success(request, 'form has being submitted')
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            print('there was an error ', f'{form.errors}')
            messages.error(request, f'{form.errors}')
            return redirect('forum:forum_detail', instance.id)

    else:
        messages.error(request, f'You have to make a post request')
    return redirect('forum:forum_detail', instance.id)
