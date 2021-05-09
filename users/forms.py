from django import forms
from django.conf import settings
from pagedown.widgets import PagedownWidget
from upload_validator import FileTypeValidator

from courses.models import Course
from memberships.models import Membership
from .models import Contact, Profile

from django.contrib.auth.models import User


class ContactAdminForm(forms.ModelForm):
    contact_name = forms.CharField(validators=[], label='', max_length=50, widget=forms.TextInput(attrs={
        'placeholder': '  Name ',
        'label': 'Name',
        'class': ' form-control     span',
    }))
    contact_email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'placeholder': ' Email ',
        'class': 'form-control    span',

    }))
    contact_subject = forms.CharField(max_length=200, label='', widget=forms.TextInput(attrs={
        'placeholder': 'Subject ',
        'class': 'form-control   ',
    }))
    contact_message = forms.CharField(max_length=1000, label='', widget=forms.Textarea(attrs={
        'placeholder': ' Content ',
        'class': 'md-textarea form-control    ',
        'rows': '5',
        'cols': '20',
    }))

    class Meta:
        model = Contact
        fields = ['contact_email', 'contact_message', 'contact_name', 'contact_subject']


class ProfileUpdateForm(forms.ModelForm):
    profile_pics = forms.ImageField(required=True, validators=[FileTypeValidator(
        allowed_types=['image/*']
    )])

    class Meta:
        model = Profile
        fields = [
            'profile_pics',
            'background_image', 'about', ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class SendMailForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=PagedownWidget())
