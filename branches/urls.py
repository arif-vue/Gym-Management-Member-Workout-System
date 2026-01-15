from django.urls import path
from . import views

urlpatterns = [
    path('', views.gym_branches, name='gym-branches'),
]
