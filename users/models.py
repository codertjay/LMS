from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.db.models.signals import post_save

from courses.models import Course

user_choices = (
    ('Student', 'Student'),
    ('Instructor', 'Instructor'),
)

User = settings.AUTH_USER_MODEL


class Contact(models.Model):
    contact_name = models.CharField(max_length=50)
    contact_email = models.EmailField(max_length=50)
    contact_subject = models.CharField(max_length=50)
    contact_message = models.TextField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=user_choices, default='Student')
    profile_pics = models.ImageField(upload_to='profile', default='profile_pics/profile.jpg')
    background_image = models.ImageField(upload_to='profile', default='profile_pics/background.jpg')
    about = models.TextField(max_length=500, blank=True, null=True)
    applied_courses = models.ManyToManyField(Course,
                                             related_name='applied_courses', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    about = models.TextField()

    def __str__(self):
        return f"{self.user.first_name} - {self.user.last_name} -({self.user.username})"

    @property
    def profilePicsImageURL(self):
        try:
            image = self.profile_pics.url
        except:
            image = None
        return image


    @property
    def backgroundImageURL(self):
        try:
            image = self.background_image.url
        except:
            image = None
        return image


def post_save_user_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    user_profile, created = Profile.objects.get_or_create(user=instance)
    if user_profile.user_type is None or user_profile.user_type == '':
        user_profile.user_type = 'Student'
        user_profile.save()


post_save.connect(post_save_user_profile_create, sender=User)
