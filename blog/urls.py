from django.urls import path
from .views import (BloglistView,
                    BlogDetailView,
                    update_post_view,
                    DeletePostView,create_comment,BlogCreateView,news_blog_list,news_blog_detail
                    )



app_name = 'blog'
urlpatterns = [

    path('#/old', BloglistView.as_view(), name='old_blog_list'),
    path('', news_blog_list, name='blog_list'),
    path('#/#/<str:sources>/',news_blog_detail,name='news_blog_detail'),
    path('#/blog_create', BlogCreateView.as_view(), name='blog_create'),
    path('<str:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('<str:slug>/comment_create', create_comment, name='comment_create'),
    path('<str:slug>/update/', update_post_view, name='update_post'),
    path('<str:slug>/delete/', DeletePostView.as_view(), name='delete_post'),

]
