from django.urls import path
from .views import CourseListView, CourseDetailView, LessonDetailView,StudentCourseListView

app_name = 'courses'
urlpatterns = [
    path('', CourseListView.as_view(), name='list'),
    path('student_course/', StudentCourseListView.as_view(), name='student_course_list'),
    path('#/<str:slug>/', CourseDetailView.as_view(), name='detail'),
    path('#/<str:course_slug>/<str:lesson_slug>/', LessonDetailView.as_view(), name='lesson_detail'),
]

