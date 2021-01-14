from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from memberships.models import Membership
from moviepy.editor import VideoFileClip

User = settings.AUTH_USER_MODEL

CourseTag = (
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advance', 'Advance')
)


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, default=1, null=True)
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    allowed_memberships = models.ManyToManyField(Membership)
    image = models.ImageField()
    rating = models.IntegerField(default=5)
    tag = models.CharField(choices=CourseTag, max_length=15, default='Intermediate')

    @property
    def imageURL(self):
        try:
            image = self.image.url
        except:
            image = None
        return image

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('courses:detail', kwargs={'slug': self.slug})

    @property
    def lessons(self):
        return self.lesson_set.all().order_by('position')
    @property
    def first_lesson(self):
        return self.lesson_set.first()

    @property
    def course_messages(self):
        return self.coursemessages_set.all()



class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video = models.FileField(upload_to='video')
    thumbnail = models.ImageField()
    duration = models.CharField(max_length=10,default='0:0')


    def __str__(self):
        return self.title

    @property
    def thumbnailURL(self):
        try:
            thumbnail = self.thumbnail.url
        except:
            thumbnail = None
        return thumbnail

    @property
    def videoURL(self):
        try:
            video = self.video.url
        except:
            video = None
        return video

    def get_absolute_url(self):
        return reverse('courses:lesson_detail',
                       kwargs={
                           'course_slug': self.course.slug,
                           'lesson_slug': self.slug
                       })

    # clip = VideoFileClip("my_video.mp4")
    # print(clip.duration)


class CourseMessages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=300)


#  Todo: admin course to the recent course once the user apply for a course
class RecentCourses(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)


def post_save_recent_courses_create(sender, instance, created, *args, **kwargs):
    if created:
        RecentCourses.objects.get_or_create(user=instance)
    recent_course, created = RecentCourses.objects.get_or_create(user=instance)


post_save.connect(post_save_recent_courses_create, sender=User)
