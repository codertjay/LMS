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
            , 'allowed_memberships'
            , 'tag'
            , 'description'
                  ]

    # def save(self, commit=True):
    #     instance = forms.ModelForm.save(self,False)
    #     old_save_m2m = self.save_m2m
    #     # fet the unsaved


class LessonCreateEditForm(forms.ModelForm):
    thumbnail = forms.ImageField(required=True, validators=[FileTypeValidator(
        allowed_types=['image/*']
    )])

    class Meta:
        model = Lesson
        fields = [
            'title', 'thumbnail', 'course', 'position', 'video',
        ]
