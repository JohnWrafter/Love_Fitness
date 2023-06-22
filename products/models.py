"""
Import Models from Database
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.db import models

# Internal:
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


class Category(models.Model):
    """
    A class for the category model
    """

    class Meta:
        """
        A meta class for the category models
        """
        verbose_name_plural = 'Categories'

    name = models.CharField(
        verbose_name=('Name'),
        max_length=254
    )
    friendly_name = models.CharField(
        max_length=254,
        null=True,
        blank=True,
    )


def __str__(self):
    """
    Returns the category name string
    Args:
    self (object): self.
    Returns:
    The category name string
    """
    return self.name


def get_friendly_name(self):
    """
    Returns the category friendly name string
    Args:
    self (object): self.
    Returns:
    The category friendly name string
    """
    return self.friendly_name


class Product(models.Model):
    """
    A class for the product model
    """
    category = models.ForeignKey(
        'Category',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(
        max_length=254
    )
    description = models.TextField(
        verbose_name=('Description')
   
    )
    has_sizes = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )
    rating = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True
    )
    image_url = models.URLField(
        verbose_name=('Image url'),
        max_length=1024,
        null=True,
        blank=True
    )
    image = models.ImageField(
        verbose_name=('Image'),
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
