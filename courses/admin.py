from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import Course, Lesson, RecentCourses


@admin.register(Course)
class ViewAdmin(ImportExportModelAdmin):
    pass


@admin.register(Lesson)
class ViewAdmin(ImportExportModelAdmin):
    pass


@admin.register(RecentCourses)
class ViewAdmin(ImportExportModelAdmin):
    pass
