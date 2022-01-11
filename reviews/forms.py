from django import forms
from .models import *


class ReviewForm(forms.ModelForm):
    """ Form for users to add reviews of products"""
    class Meta:
        model = Review
        fields = ('rating', 'title', 'comment',)