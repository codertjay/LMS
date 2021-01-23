from django import forms
from pagedown.widgets import PagedownWidget
from .models import Post
from .models import Comment

from upload_validator import FileTypeValidator


class PostCreateForm(forms.ModelForm):
    description = forms.CharField(widget=PagedownWidget())
    published_date = forms.DateField(widget=forms.SelectDateWidget)
    image = forms.ImageField(required=True, validators=[FileTypeValidator(
        allowed_types=['image/*']
    )])

    class Meta:
        model = Post
        fields = ['title', 'category', 'image', 'published_date', 'description']


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
