"""
Model form blog form
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from datetime import datetime, date
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Internal:

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Post(models.Model):
    """
    A class for the blog model
    """
    title = models.CharField(
        verbose_name=('Name'),
        max_length=255
    )
    title_tag = models.CharField(
        max_length=255
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    body = models.TextField(
        verbose_name=('Name')
    )
    post_date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title + ' | ' + str(self.author)
