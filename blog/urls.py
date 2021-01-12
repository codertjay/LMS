from django.urls import path
from .views import (BloglistView,
                    BlogDetailView,
                    update_post_view,
                    DeletePostView,
                    )



app_name = 'blog'
urlpatterns = [
    path('', BloglistView.as_view(), name='blog_list'),
    path('<str:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('<str:slug>/update/', update_post_view, name='update_post'),
    path('<str:slug>/delete/', DeletePostView.as_view(), name='delete_post'),

]