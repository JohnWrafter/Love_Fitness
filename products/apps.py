"""
A class for the prodcuts app
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.apps import AppConfig

# Internal
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class LoveFitnessConfig(AppConfig):
    name = 'love-fitness' 

class ProductsConfig(AppConfig):
    """
    A class for the product app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
