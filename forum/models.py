from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
from django.utils.safestring import mark_safe
from markdown_deux import markdown

User = settings.AUTH_USER_MODEL


class ForumManager(models.Manager):
    def top_forums(self):
        forum_qs = self.all().order_by('-view_count')
        return forum_qs


class ForumQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    view_count = models.IntegerField(default=0)
    objects = ForumManager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('forum:forum_detail', kwargs={'pk': self.pk})

    @property
    def forum_answers(self):
        answers = self.forumanswer_set.all()
        return answers

    @property
    def get_markdown(self):
        description = self.content
        markdown_text = markdown(description)
        return mark_safe(markdown_text)


class ForumAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    forum_question = models.ForeignKey(ForumQuestion, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} + {self.forum_question.title}"

    @property
    def get_markdown(self):
        description = self.content
        markdown_text = markdown(description)
        return mark_safe(markdown_text)
