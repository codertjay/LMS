from django.urls import path
from .views import StudentDashBoardView,InstructorDashBoardView

app_name = 'users'
urlpatterns = [
    path('student_dashboard/', StudentDashBoardView.as_view(), name='student_dashboard'),
    path('instructor_dashboard/', InstructorDashBoardView.as_view(), name='instructor_dashboard'),
]
