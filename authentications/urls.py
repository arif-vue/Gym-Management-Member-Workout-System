from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.login),
    path('refresh-token/', views.refresh_token),
    path('profile/', views.get_profile),
    
    # User Management (Admin & Manager)
    path('users/', views.users),
]
