from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    # Post Form
    class Meta:
        model = Post
        fields = ['title', 'intro', 'image', 'body']

    image = forms.ImageField(
        label="Image",
        required=False,
        )


class CommentForm(forms.ModelForm):
    # Comment Form
    class Meta:
        model = Comment
        fields = ['body']