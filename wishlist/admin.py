"""
Set fields admin view
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.contrib import admin

# Internal:
from .models import Favourites

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class FavouritesAdmin(admin.ModelAdmin):
    """
    List of fields to display in Django Admin
    """
    list_display = (
        'username',
    )


    ordering = ('username',)


admin.site.register(Favourites, FavouritesAdmin)
