from django.contrib import admin

# Register your models here.
from memberships.models import UserMembership, Membership

admin.site.register(Membership)
admin.site.register(UserMembership)