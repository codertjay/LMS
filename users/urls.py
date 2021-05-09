from django.urls import path

from .views import InstructorDashBoardView, contactAdminView, public_profile_view, UserProfileUpdate, InstructorSendMail

app_name = 'users'
urlpatterns = [
    path('instructor_dashboard/', InstructorDashBoardView.as_view(), name='instructor_dashboard'),
    path('contact/', contactAdminView, name='contact'),
    path('sendmail/', InstructorSendMail.as_view(), name='send_mail'),

    # academy profile
    path('profile/<str:username>/', public_profile_view, name='profile'),
    path('profile_update/', UserProfileUpdate.as_view(), name='profile_edit'),
    path('profile_update/', UserProfileUpdate.as_view(), name='profile_edit'),

]
