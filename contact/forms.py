"""
Config for contact forms
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django import forms

# Internal
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Configure contact us form
    """
    class Meta:
        """
        Configure meta data contact form
        """
        model = Contact

        fields = "__all__"
