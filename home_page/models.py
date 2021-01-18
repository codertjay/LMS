from django.db import models


# Create your models here.


class Subscribe(models.Model):
    email = models.EmailField()


class Testimonial(models.Model):
    name = models.CharField(max_length=30)
    title = models.CharField(max_length=40)
    image = models.ImageField(blank=True, null=True)
    content = models.CharField(max_length=500)

    @property
    def imageURL(self):
        try:
            image = self.image.url
        except:
            image = None
        return image
