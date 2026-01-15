from django.urls import path
from . import views

urlpatterns = [
    # Workout Plans
    path('plans/', views.workout_plans, name='workout-plans'),
    
    # Workout Tasks
    path('tasks/', views.workout_tasks, name='workout-tasks'),
    path('tasks/<int:task_id>/', views.update_task_status, name='update-task-status'),
]
