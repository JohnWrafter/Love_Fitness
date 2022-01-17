from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class Favourites(models.Model):
    """
    This model is for a users wishlist
    """
    class Meta:
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
