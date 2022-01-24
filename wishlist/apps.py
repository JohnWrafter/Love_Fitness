"""
Import appconfig for Wish List
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.apps import AppConfig


class WishlistConfig(AppConfig):
    """
    A class for the Wish List app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wishlist'
