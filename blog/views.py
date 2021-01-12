from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView, View, DetailView

from .forms import CommentForm
from .models import Comment
from .forms import PostCreateForm
from .models import Post
from .utils import get_read_time


# Create your views here.


class BloglistView(ListView):
    model = Post
    queryset = Post.objects.published()
    template_name = 'HomePage/blog.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        post = Post.objects.all()
        if query:
            object_list = post.filter(
                Q(category__icontains=query) |
                Q(description__icontains=query) |
                Q(user__username__icontains=query) |
                Q(title__icontains=query)
            ).distinct()
        else:
            object_list = Post.objects.all()
        return object_list


class BlogUserListView(ListView):
    model = Post
    template_name = 'HomePage/blog.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(user=user)


class BlogDetailView(DetailView):
    template_name = 'HomePage/detail-blog.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = context['object']
        """ note this instance.get_content_type is from our models where we 
        linked the comment models and the blog models with content_type and object_id """

        print('read time :', get_read_time(instance.description))
        print('read time :', get_read_time(instance.get_markdown()))

        context['form'] = CommentForm()
        return context


@login_required
def create_comment(request, slug=None):
    try:
        instance = Post.objects.get(slug=slug)
    except ObjectDoesNotExist:
        instance = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        print('The form data :', form)
        if form.is_valid():
            print(form.cleaned_data)
            form_data = form.save(commit=False)
            form_data.user = request.user
            form_data.post = instance
            form.save()
            messages.success(request, 'form has being submitted')
            return HttpResponseRedirect(instance.get_absolute_url())
        else:
            print('there was an error ', f'{form.errors}')
            messages.error(request, f'{form.errors}')
            return redirect('blog:blog_detail', instance.slug)

    else:
        messages.error(request, f'You have to make a post request')
    return redirect('blog:blog_detail', instance.slug)


class BlogCreateView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        form = PostCreateForm()
        return render(self.request, 'blog/blog_create.html', {'forms': form})

    def post(self, *args, **kwargs):
        form = PostCreateForm(self.request.POST, self.request.FILES or None)
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
        return redirect('blog_create')


@login_required
def update_post_view(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    form = PostCreateForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        print(instance.read_time)
        print(instance.slug)
        print(instance.slug)
        instance.save()
        print('updating the post', request.POST, '\n', instance.user)
        messages.success(request, 'The form is  valid')
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.warning(request, 'The form isn\'t valid')

    return render(request, 'HomePage/Update-blog.html', {'form': form})


class DeletePostView(DeleteView):
    model = Post
    template_name = 'HomePage/delete-blog.html'
    success_url = '/'
