""" Import AppConfig from DjangoApps """
from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """ Config BigAutoField for Profiles app SS"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'
