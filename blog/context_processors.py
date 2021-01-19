from .models import Post


def add_variable_to_context(try_content=None):
    latest_posts = Post.objects.all()
    older_posts = Post.objects.all().order_by('id')
    if Post.objects.count() > 6:
        latest_posts = Post.objects.all()[3]
    if Post.objects.count() > 6:
        older_posts = Post.objects.all().order_by('id')[3]
    print(latest_posts)
    return {'older_posts': older_posts,
            'latest_posts': latest_posts,
            'instagram_url': 'http:instagram.com'
            }


