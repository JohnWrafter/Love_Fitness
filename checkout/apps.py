"""
Import AppConfig
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """
    Signals for Checkout App
    """
    name = 'checkout'

    def ready(self):
        import checkout.signals
