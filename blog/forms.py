from django import forms
from .models import Post
from .models import Comment
from django_quill.forms import QuillFormField

from upload_validator import FileTypeValidator


class PostCreateForm(forms.ModelForm):
    description = QuillFormField()
    published_date = forms.DateField(widget=forms.SelectDateWidget)

    image = forms.ImageField(required=True, validators=[FileTypeValidator(
        allowed_types=['image/*']
    )],
                             widget=forms.FileInput(attrs={
                                 'class': '  waves-effect   bg-primary   ',

                             }))

    class Meta:
        model = Post
        fields = ['title'
            , 'slug'
            , 'category'
            , 'description'
            , 'image'
            , 'published_date']


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control   ',
        'placeholder': "Write some nice stuff or nothing...",
        'cols': '40',
        'rows': '4'
    }))

    class Meta:
        model = Comment
        fields = ['content']
