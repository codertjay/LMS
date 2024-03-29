from django import forms
from upload_validator import FileTypeValidator

from .models import Course, Lesson
from memberships.models import Membership, MembershipType


class CourseCreateEditForm(forms.ModelForm):
    allowed_memberships = forms.ModelMultipleChoiceField(
        queryset=Membership.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    image = forms.ImageField(required=True, validators=[FileTypeValidator(
        allowed_types=['image/*']
    )])

    class Meta:
        model = Course
        fields = ['title'
            , 'image'
            , 'course_language'
            , 'allowed_memberships'
            , 'description']


class LessonCreateEditForm(forms.ModelForm):
    thumbnail = forms.ImageField(required=True, validators=[FileTypeValidator(
        allowed_types=['image/*']
    )])
    video = forms.FileField(required=True, validators=[FileTypeValidator(
        allowed_types=['video/*']
    )])

    class Meta:
        model = Lesson
        fields = [
            'title', 'thumbnail', 'course', 'position', 'video',
        ]

class LessonEditForm(forms.ModelForm):
    thumbnail = forms.ImageField(required=True, validators=[FileTypeValidator(
        allowed_types=['image/*']
    )])
    class Meta:
        model = Lesson
        fields = [
            'title', 'thumbnail', 'course', 'position', 'video',
        ]
