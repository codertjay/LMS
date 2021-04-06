from django.urls import path

from academy_dashboard.views import CourseListView, LessonDetailView, CourseDetailView

urlpatterns = [
    # courses
    path('', CourseListView.as_view(), name='course_list'),
    path('#/<str:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('<str:course_slug>/<str:lesson_slug>/', LessonDetailView.as_view(), name='lesson_detail'),



]

