from .models import Comment, Post, Message
from django import forms
from django_summernote.widgets import SummernoteWidget


class CommentForm1(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')

class CommentForm2(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'status', 'author', 'language', 'quotation', 'thumb','content')
        widgets = {'content': SummernoteWidget()}


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'status', 'author', 'language', 'quotation', 'thumb','content')
        widgets = {'content': SummernoteWidget()}


class UserLoginForm(forms.Form):
    username = forms.CharField(label="User name")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('email', 'subject', 'content')
    

# class MailForm(forms.ModelForm):
#     class Meta:
#         model = Mail
#         fields = ('subject', 'content')