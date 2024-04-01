from django import forms
from .models import Post, Comment


class UserPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']

