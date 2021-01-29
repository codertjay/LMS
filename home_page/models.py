from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Subscribe(models.Model):
    email = models.EmailField()


class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=40)
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
