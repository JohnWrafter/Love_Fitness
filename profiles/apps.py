"""
Import AppConfig from DjangoApps
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """
    A class for configuring the profiles app
    """
    name = 'profiles'
