from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login),
    path('refresh-token/', views.refresh_token),
    path('profile/', views.get_profile),
    
    # Gym Branch Management (Admin only)
    path('gym-branches/', views.gym_branches),
    
    # User Management (Admin & Manager)
    path('users/', views.users),
]
