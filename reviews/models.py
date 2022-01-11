from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils import timezone


# Review system model
class Review(models.Model):
    '''
        got help with rating choices and model in general from
        https://www.codementor.io/@jadianes/get-started-with-django-building-recommendation-review-app-du107yb1a
        and https://www.youtube.com/watch?v=lSX8nzu9ozg
    '''
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=254, null=False, blank=False, default='')
    comment = models.TextField(max_length=1000, null=False, blank=False)
    rating = models.IntegerField(choices=RATING_CHOICES,
                                 null=False,
                                 blank=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review on {self.product.name} by {self.user}"

    class Meta:
        ordering = ['id']