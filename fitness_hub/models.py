from django.db import models

class FitnessHub(models.Model):
    name = models.CharField(max_length=254, default=False, null=True, blank=True)
    text = models.TextField(null=True)
    message = models.TextField(null=False, blank=False, default=False)

    def __str__(self):
        return self.name