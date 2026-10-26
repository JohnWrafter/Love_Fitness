"""
URLs for Home page
"""
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from django.urls import path

# Ineternal:
from . import views
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

urlpatterns = [
    path('', views.index, name="home"),
    path('product-finder/', views.product_finder, name='product_finder'),
    path('workout-routine/', views.workout_routine, name='workout_routine'),
    path('nutrition-plan/', views.nutrition_plan, name='nutrition_plan'),
]
