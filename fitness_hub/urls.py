from django.urls import path
from . import views

urlpatterns = [
    path('', views.Fitness, name='fitness_hub'),
]