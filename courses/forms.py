from django import forms
from .models import Course


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['slug'
            , 'title'
            , 'description'
            , 'allowed_memberships'
            , 'image'
            , 'rating'
            , 'tag']
