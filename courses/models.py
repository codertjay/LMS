from django.db import models
from django.urls import reverse

from memberships.models import Membership


class Course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    allowed_memberships = models.ManyToManyField(Membership)
    image = models.ImageField()

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


class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    position = models.IntegerField()
    video = models.FileField(upload_to='video')
    thumbnail = models.ImageField()

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
