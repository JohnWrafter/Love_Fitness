from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='plans'),
    path('<int:plan_id>/', views.plans_detail, name='plans_detail'),
]
