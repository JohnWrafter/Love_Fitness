from django.contrib import admin

from .models import FitnessHub

list_display = (
        'name',
        'text',
        'message',
    )

admin.site.register(FitnessHub)