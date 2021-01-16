from django.urls import path
from .views import (ForumQuestionCreateView,
                    ForumQuestionDeleteView,
                    ForumQuestionDetailView,
                    forum_answer_create_view,ForumListView
                    )

app_name = 'forum'
urlpatterns = [
    path('', ForumListView.as_view(), name='forum_list'),
    path('forum_create/', ForumQuestionCreateView.as_view(), name='forum_create'),
    path('<int:pk>/', ForumQuestionDetailView.as_view(), name='forum_detail'),
    path('<int:pk>/delete/', ForumQuestionDeleteView.as_view(), name='forum_delete'),
    path('<int:pk>/forum_answer_create/', forum_answer_create_view, name='forum_answer_create'),
]
