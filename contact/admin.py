"""
Admin fields config for contact app
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.contrib import admin

# Internal:
from .models import Contact
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class ContactAdmin(admin.ModelAdmin):
    """
    List of fields to display in Django Admin
    """
    list_display = (
        'full_name',
        'subject',
        'email',
        'message',
    )

    ordering = ('full_name',)


admin.site.register(Contact, ContactAdmin)
