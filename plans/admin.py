from django.contrib import admin
from .models import Exercise, Nutrition

# Register your models here.


class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
        'plan',
        'price',
        'rating',
        'image',
    )
    ordering = ('name',)


class NutritionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
        'plan',
        'price',
        'rating',
        'image',
    )


admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Nutrition, NutritionAdmin)
