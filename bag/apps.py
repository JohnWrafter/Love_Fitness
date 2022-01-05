""" Import AppConfig from Django Apps"""
from django.apps import AppConfig


class BagConfig(AppConfig):
    """ BigAutoField config for Bag app """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bag'
