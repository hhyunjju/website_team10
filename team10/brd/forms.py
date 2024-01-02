from django import forms
from .models import Post, Comment

# class PostForm(forms.Form):
#     title = forms.CharField(label='제목')
#     body = forms.CharField(label='내용', widget=forms.Textarea)
    
#view-> post_create에서 사용
class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'photo']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
