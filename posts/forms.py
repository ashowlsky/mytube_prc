from django import forms
from posts.models import Post, Group, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
