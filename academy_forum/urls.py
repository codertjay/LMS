from django.urls import path
from .views import (ForumQuestionCreateView,
                    ForumQuestionDetailView,
                    forum_answer_create_view,
                    ForumListView,
                    ForumQuestionDeleteView,
                    ForumQuestionUpdateView, forum_update_view
                    )

app_name = 'academy_forum'
urlpatterns = [
    path('forum/forum_list/#/', ForumListView.as_view(), name='forum_list'),
    path('forum/forum_create/#/', ForumQuestionCreateView.as_view(), name='forum_create'),
    path('forum/<int:pk>/#/', ForumQuestionDetailView.as_view(), name='forum_detail'),
    path('<int:pk>/delete/#/', ForumQuestionDeleteView.as_view(), name='forum_delete'),
    path('<int:id>/update/#/', forum_update_view, name='forum_update'),
    path('<int:pk>/forum_answer_create/#/', forum_answer_create_view, name='forum_answer_create'),
]
