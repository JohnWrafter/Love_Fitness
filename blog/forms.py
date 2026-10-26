"""
Blog App configuration
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django import forms

# Internal:
from .models import Post

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ArticleAssistantForm(forms.Form):
    query = forms.CharField(
        max_length=250,
        label='What would you like to read about?',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'For example: getting started with strength training',
        }),
    )
    consent = forms.BooleanField(
        label='I agree to send my request to OpenAI to find relevant articles.',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )


class PostForm(forms.ModelForm):
    """
    Blog form for posting blogs
    """
    class Meta:
        """
        Blog form fields config
        """
        model = Post
        fields = (
            'title',
            'title_tag',
            'body'
        )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }


class EditForm(forms.ModelForm):
    """
    Blog form for editing blogs
    """
    class Meta:
        """
        Blog form fields for editing blog
        """
        model = Post
        fields = (
            'title',
            'title_tag',
            'body'
        )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
