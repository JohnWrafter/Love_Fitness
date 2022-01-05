""" Import AppConfig from Django Apps """
from django.apps import AppConfig


class HomeConfig(AppConfig):
    """ BigAutoField config for Home appS """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
