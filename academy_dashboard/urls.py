from django.urls import path

from academy_dashboard.views import CourseListView, LessonDetailView, CourseDetailView, StudentCourseTypeView, \
    academy_subscribe_view

urlpatterns = [
    # courses
    path('', CourseListView.as_view(), name='course_list'),
    path('<str:course_type>/', StudentCourseTypeView.as_view(), name='course_type'),
    path('#/<str:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('<str:course_slug>/<str:lesson_slug>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('subscribe/academy/#/', academy_subscribe_view, name='academy_subscribe_view'),

]
