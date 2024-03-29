from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, DetailView, UpdateView
from django.views.generic.base import View

from .forms import ForumAnswerForm, ForumQuestionForm
from .models import ForumQuestion
from django_hosts.resolvers import reverse as host_reverse


class ForumListView(LoginRequiredMixin, ListView):
    model = ForumQuestion
    template_name = 'StudentDashboard/forum/student-forum.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search')
        forum = ForumQuestion.objects.all()
        if query:
            object_list = forum.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        else:
            object_list = ForumQuestion.objects.all()
        return object_list


class ForumQuestionCreateView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        form = ForumQuestionForm()
        forum = ForumQuestion.objects.all()[:4]
        return render(self.request, 'StudentDashboard/forum/student-forum-ask.html',
                      {'form': form, 'academy_forum': forum})

    def post(self, *args, **kwargs):
        form = ForumQuestionForm(self.request.POST)
        print(self.request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.save()
            messages.success(self.request, 'Question was created ')
            return HttpResponseRedirect(instance.get_absolute_url())

        elif not form.is_valid():
            messages.error(self.request, 'invalid form data')
        return redirect('forum:forum_create')


class ForumQuestionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'StudentDashboard/forum/student-forum-detail.html'
    model = ForumQuestion
    context_object_name = 'forum_question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = context['object']
        instance.view_count += 1
        instance.save()
        forumquestion_list = ForumQuestion.objects.all()[:10]
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
        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.forum_question = instance
            form.save()
            messages.success(request, 'You have successfully answer the question ')
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            print('there was an error ', f'{form.errors}')
            messages.error(request, f'{form.errors}')
            return redirect('forum:forum_detail', instance.id)

    else:
        messages.error(request, f'There was an error ')
    return redirect('forum:forum_detail', instance.id)


class ForumQuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ForumQuestion
    template_name = 'StudentDashboard/forum/forum-update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user or self.request.user.is_superuser:
            return True
        return False

    def get_success_url(self):
        return redirect('forum:forum_detail')


class ForumQuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ForumQuestion
    template_name = 'StudentDashboard/forum/forum-delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user or self.request.user.is_superuser:
            return True
        return False

    def get_success_url(self):
        return host_reverse('forum_list', host='academy', )


@login_required
def forum_update_view(request, id=None):
    instance = get_object_or_404(ForumQuestion, id=id)
    form = ForumQuestionForm(request.POST or None, request.FILES or None, instance=instance)
    if request.user == instance.user or request.user.is_superuser:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'The form is  valid')
            return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.warning(request, 'The form isn\'t valid')
    context = {'form': form, 'object': instance}
    return render(request, 'StudentDashboard/forum/forum-update.html', context)
