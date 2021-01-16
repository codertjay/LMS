from django.urls import path
from .views import StudentDashBoardView, InstructorDashBoardView, UserProfileUpdate, public_profile_view

app_name = 'users'
urlpatterns = [
    path('student_dashboard/', StudentDashBoardView.as_view(), name='student_dashboard'),
    path('instructor_dashboard/', InstructorDashBoardView.as_view(), name='instructor_dashboard'),
    path('#/<str:username>/', public_profile_view, name='profile'),
    path('profile_update/', UserProfileUpdate.as_view(), name='profile_edit'),
]
