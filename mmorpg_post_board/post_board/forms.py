from django import forms
from .models import Post, Reply
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = [
           'header',
           'content',
           'category',
       ]


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = [
            'text',
        ]


