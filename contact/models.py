"""
A model for the contact app
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.db import models

# Internal:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Contact(models.Model):
    """
    Contact model and text fields
    """
    full_name = models.CharField(
        max_length=120,
        null=False,
        blank=False,
        default=""
    )
    subject = models.CharField(
        max_length=120,
        null=False,
        blank=False
    )
    email = models.EmailField(
        max_length=254,
        null=False,
        blank=False
    )
    message = models.TextField(
        null=False,
        blank=False
    )

    def __str__(self):
        return self.subject
