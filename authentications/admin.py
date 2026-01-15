from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, GymBranch


@admin.register(GymBranch)
class GymBranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'created_at']
    search_fields = ['name', 'location']


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'email', 'role', 'gym_branch', 'is_active', 'created_at']
    list_filter = ['role', 'gym_branch', 'is_active']
    search_fields = ['email']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Role & Branch', {'fields': ('role', 'gym_branch')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'gym_branch'),
        }),
    )
