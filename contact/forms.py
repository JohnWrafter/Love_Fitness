"""
Config for contact forms
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Configure contact us form
    """
    class Meta:
        """
        Meta config for contact form
        """
        model = Contact

        fields = "__all__"
