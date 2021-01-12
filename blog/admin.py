from django.contrib import admin
from.models import Post,Action,Comment
# Register your models here.


class ActionAdmin(admin.TabularInline):
    model = Action

class PostAdminModel(admin.ModelAdmin):
    inlines = [ActionAdmin]


admin.site.register(Post,PostAdminModel)
admin.site.register(Comment)