"""
Set fields admin view
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.contrib import admin

# Internal:
from .models import Post

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class PostAdmin(admin.ModelAdmin):
    """
    List of fields to display in Django Admin
    """
    list_display = (
        'title',
        'title_tag',
        'author',
        'body',
    )

    ordering = ('author',)


admin.site.register(Post, PostAdmin)
