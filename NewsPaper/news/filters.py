from django_filters import FilterSet, CharFilter, DateFilter
from django import forms
from .models import Post

class PostFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название статьи',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Поиск по названию...'
        })
    )
    author_name = CharFilter(
        field_name='author__username',
        lookup_expr='icontains',
        label='Имя автора содержит',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя автора...'
        })
    )
    
    created_date = DateFilter(
        field_name='created_at',
        lookup_expr='gte',  # gte = greater than or equal (позже или равно)
        label='Опубликовано после',
        widget=forms.DateInput(
            attrs={
                'type': 'date',  # Включает календарь в браузере
                'class': 'form-control',
            }
        )
    )
    
    class Meta:
        model = Post
        fields = []  # Все поля определены выше