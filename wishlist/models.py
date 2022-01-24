"""
Import Models and user
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.db import models
from django.contrib.auth.models import User

# Internal:
from products.models import Product
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Favourites(models.Model):
    """
    This model is for a users wishlist
    """
    class Meta:
        """
        A class for the Wish list app
        """
        verbose_name_plural = 'Wishlists'

    products = models.ManyToManyField(
        Product,
        blank=True
    )
    username = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        """
        Returns user wishlist
        """
        return f"{self.username}'s Wishlist"
