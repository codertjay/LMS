from django.contrib import admin
from .models import ForumAnswer, ForumQuestion

admin.site.register(ForumAnswer)
admin.site.register(ForumQuestion)
