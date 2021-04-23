from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.urls import reverse
from django.utils.text import slugify
from moviepy.editor import VideoFileClip

from memberships.models import Membership
from django.contrib.auth.models import User
from django_hosts.resolvers import reverse as host_reverse

def convert(n):
    return str(timedelta(seconds=n))


def video_clip_duration(video_path):
    print('this is the video path', video_path)
    clip = VideoFileClip(video_path)
    print('this is the video clip', clip)
    duration = clip.duration
    print('this is the video duration', duration)
    return duration


Courselanguage = (
    ('ENGLISH', 'ENGLISH'),
    ('SPANISH', 'SPANISH'),
)



class CourseManager(models.Manager):
    pass


class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    course_language = models.CharField(choices=Courselanguage, max_length=20, default="English")
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=120)
    description = models.TextField()
    allowed_memberships = models.ManyToManyField(Membership)
    image = models.ImageField()
    rating = models.IntegerField(default=5)
    view_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CourseManager()

    def get_absolute_url(self):
        return host_reverse('course_detail', args=(self.slug,), host='academy',)

    class Meta:
        ordering = ['-id']

    @property
    def imageURL(self):
        try:
            image = self.image.url
        except:
            image = None
        return image

    def __str__(self):
        return self.title

    @property
    def course_tag(self):
        return CourseTag

    @property
    def related_courses(self):
        course_list = Course.objects.filter(title=self.title)[:4]
        print('the course list', course_list)
        return course_list

    @property
    def lessons(self):
        return self.lesson_set.all().order_by('position')

    @property
    def course_duration(self):
        duration = 0
        try:
            for item in self.lessons:
                if item.video:
                    duration += video_clip_duration(item.video.path)
                    print('this is the duration of the video', duration)
            print('this is the course duration of the video', duration)
        except:
            duration = 0
        return convert(duration)

    @property
    def first_lesson(self):
        return self.lesson_set.first()

    @property
    def course_messages(self):
        return self.coursemessages_set.all()


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = f'{slug, qs.first().id}'
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_course_receiver(sender, instance, *args, **kwargs):
    print('trying to create the slug', )
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_course_receiver, sender=Course)


class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video = models.FileField(upload_to='video')
    video_response = models.CharField(max_length=300)
    thumbnail = models.ImageField(upload_to='lesson_thumbnail', default='lesson_thumbnail/thumbnail.jpg')
    timestamp = models.DateTimeField(auto_now_add=True)

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

    @property
    def duration(self):
        try:
            # Todo: change this to url when you try to push the project
            duration = video_clip_duration(self.video.path)
        except:
            duration = 0
        print('the duration of the video ', duration)
        return convert(duration)

    def get_absolute_url(self):
        return reverse('courses:lesson_detail',
                       kwargs={
                           'course_slug': self.course.slug,
                           'lesson_slug': self.slug
                       })


def create_lesson_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Lesson.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = f'{slug, qs.first().id}'
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_lesson_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Lesson)


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
