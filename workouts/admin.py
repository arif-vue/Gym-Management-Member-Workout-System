from django.contrib import admin
from .models import WorkoutPlan, WorkoutTask


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_by', 'gym_branch', 'created_at']
    list_filter = ['gym_branch', 'created_by']
    search_fields = ['title', 'description']
    ordering = ['-created_at']


@admin.register(WorkoutTask)
class WorkoutTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'workout_plan', 'member', 'status', 'due_date', 'created_at']
    list_filter = ['status', 'workout_plan__gym_branch']
    search_fields = ['workout_plan__title', 'member__email']
    ordering = ['-created_at']
