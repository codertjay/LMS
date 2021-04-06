from django.urls import path

from .views import CourseCreateView, \
    LessonCreateView, course_update_view, CourseDeleteView, lesson_update_view, LessonDeleteView

app_name = 'courses'

urlpatterns = []
AdminUrlPatterns = [
    path('create_lesson/', LessonCreateView.as_view(), name='create_lesson'),
    path('#/<str:slug>/update/', course_update_view, name='update_course'),
    path('#/<str:slug>/delete/', CourseDeleteView.as_view(), name='delete_course'),
    path('#/<str:slug>/update_lesson/', lesson_update_view, name='lesson_update'),
    path('#/<str:slug>/delete_lesson/', LessonDeleteView.as_view(), name='lesson_delete'),
    path('create_course/', CourseCreateView.as_view(), name='create_course'),

]
urlpatterns += AdminUrlPatterns
