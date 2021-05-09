from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Subscribe(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


class Testimonial(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(blank=True, null=True)
    content = models.TextField()

    @property
    def imageURL(self):
        try:
            image = self.image.url
        except:
            image = None
        return image

    def get_absolute_url(self):
        return reverse('home:testimonial_create')


class ComingSoon(models.Model):
    coming_soon = models.BooleanField(default=True)
