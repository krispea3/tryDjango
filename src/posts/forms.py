""" Forms for posts """
from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    """Form for posts"""
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
        ]
