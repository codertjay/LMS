from django import forms

from .models import ForumAnswer, ForumQuestion


class ForumQuestionForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control   ',
        'placeholder': "Describe you question in full",
        'cols': '40',
        'rows': '4'
    }))

    class Meta:
        model = ForumQuestion
        fields = ['title', 'content']


class ForumAnswerForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={
        'class': 'form-control   ',
        'placeholder': "Write some nice stuff ...",
        'cols': '40',
        'rows': '4'
    }))

    class Meta:
        model = ForumAnswer
        fields = ['content']
