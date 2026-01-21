from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'content'
        ]
class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'content'
        ]

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'content'
        ]

