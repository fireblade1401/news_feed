from django import forms
from django.forms import TextInput, Textarea, ClearableFileInput, ModelChoiceField, ModelMultipleChoiceField

from .models import Article, Category, Tags, Comments, Author


class ArticleForm(forms.ModelForm):
    category = ModelChoiceField(queryset=Category.objects.all(), empty_label="Выберите категорию",
                                widget=forms.Select(attrs={'class': 'form-control'}))
    author = ModelChoiceField(queryset=Author.objects.all(), empty_label="Выберите автора",
                              widget=forms.Select(attrs={'class': 'form-control'}))
    tags = ModelMultipleChoiceField(queryset=Tags.objects.all(),
                                    widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model = Article
        fields = ['title', 'summary', 'content', 'author', 'category', 'image_url', 'tags']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'label': 'Название',
                'placeholder': 'Название статьи',
            }),
            "summary": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Анонс статьи'
            }),
            "content": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание статьи'
            }),
            "author": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Автор статьи'
            }),
            "category": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Категория статьи'
            }),
            "image_url": ClearableFileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Картинка статьи'
            }),
            "tags": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Тэги статьи'
            }),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    widgets = {
        "category_name": Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Название категории'
        }),
        "description": Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Описание категории'
        }),
    }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
