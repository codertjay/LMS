import os
from datetime import timedelta
from os import path
from time import sleep

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils.text import slugify
from django_hosts.resolvers import reverse as host_reverse
from moviepy.editor import VideoFileClip

from Learning_platform.settings import VIMEO_AUTHENTICATE
from memberships.models import Membership
import datetime


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
        return host_reverse('course_detail', args=(self.slug,), host='academy', )

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
                if item.duration:
                    # duration += video_clip_duration(item.video.path)
                    duration += VIMEO_AUTHENTICATE.get(item.video_uri).json().get('duration')
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
    video = models.FileField(blank=True, null=True, upload_to='video', )
    video_uri = models.CharField(max_length=300)
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
            video_response = VIMEO_AUTHENTICATE.get(self.video_uri)
            if video_response:
                video = video_response.json().get('link')
        except:
            video = None
        return video

    @property
    def video_iframe(self):
        try:
            video_response = VIMEO_AUTHENTICATE.get(self.video_uri)
            print('the video response', video_response)
            video = video_response.json().get("embed").get("html")
            print(video)
        except:
            video = None
        return video

    @property
    def duration(self):
        global duration
        try:
            # Todo: change this to url when you try to push the project
            # duration = video_clip_duration(self.videoURL)
            duration_response = VIMEO_AUTHENTICATE.get(self.video_uri)
            if duration_response:
                duration = duration_response.json().get('duration')
        except:
            duration = 0
        print('the duration of the video ', duration)
        return convert(duration)

    def get_absolute_url(self):
        return host_reverse('lesson_detail', args=(self.course.slug, self.slug,), host='academy')


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


def post_save_video(sender, instance, *args, **kwargs):
    if instance.video:
        video_path = instance.video.path
        path_exist = path.exists(video_path)
        print('the path exist', path_exist)
        print('the path ', video_path)
        while not path_exist:
            sleep(15)
        try:
            if path_exist:
                video_uri = None
                if not instance.video_uri:
                    video_uri = VIMEO_AUTHENTICATE.upload(
                        video_path,
                        data={'download': False, "name": instance.title}
                    )
                elif instance.video_uri:
                    video_uri = VIMEO_AUTHENTICATE.replace(
                        video_uri=instance.video_uri,
                        filename=instance.video.path
                    )
                print('successful', video_uri)
                instance.video_uri = video_uri
                instance.video = None
                instance.save()
                os.remove(video_path)
        except Exception as a:
            print(a)


post_save.connect(post_save_video, sender=Lesson)


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
