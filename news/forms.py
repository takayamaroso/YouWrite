from django import forms

from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Article
        fields = ('title', 'text', 'image')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text', 'evaluation_value')

class Search(forms.Form):
    search = forms.CharField(max_length=50)