from django.urls import path
from .views import CourseListView, CourseDetailView, LessonDetailView, StudentCourseListView, CourseCreateView, \
    LessonCreateView,course_update_view,CourseDeleteView,lesson_update_view,LessonDeleteView

app_name = 'courses'
urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('student_course/', StudentCourseListView.as_view(), name='student_course_list'),
    path('create_course/', CourseCreateView.as_view(), name='create_course'),
    path('create_lesson/', LessonCreateView.as_view(), name='create_lesson'),
    path('#/<str:slug>/update/', course_update_view, name='update_course'),
    path('#/<str:slug>/delete/', CourseDeleteView.as_view(), name='delete_course'),
    path('#/<str:slug>/', CourseDetailView.as_view(), name='detail'),
    path('<str:course_slug>/<str:lesson_slug>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('#/<str:slug>/update_lesson/', lesson_update_view, name='lesson_update'),
    path('#/<str:slug>/delete_lesson/', LessonDeleteView.as_view(), name='lesson_delete'),
]
