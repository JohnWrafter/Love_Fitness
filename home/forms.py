from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """ Configure contact us form """
    class Meta:
        model = Contact

        fields = "__all__"