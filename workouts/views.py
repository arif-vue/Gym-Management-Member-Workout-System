from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import WorkoutPlan, WorkoutTask
from .serializers import (
    WorkoutPlanSerializer,
    WorkoutPlanCreateSerializer,
    WorkoutTaskSerializer,
    WorkoutTaskCreateSerializer,
    WorkoutTaskUpdateSerializer,
)
from authentications.permissions import IsTrainer, IsAdminOrManagerOrTrainer, IsMember


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


def success_response(message, data=None, code=200):
    return Response({"success": True, "message": message, "data": data}, status=code)


def error_response(message, errors=None, code=400):
    return Response({"success": False, "message": message, "errors": errors or {}}, status=code)


# ==================== Workout Plans ====================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def workout_plans(request):
    """
    GET: List workout plans
        - Admin: All plans
        - Manager: Plans in their branch
        - Trainer: Plans in their branch
        - Member: Not allowed
    POST: Create workout plan (Trainer only)
    """
    user = request.user

    if request.method == 'GET':
        # Member cannot view workout plans
        if user.role == 'member':
            return error_response(message="Members cannot view workout plans", code=403)

        if user.role == 'admin':
            queryset = WorkoutPlan.objects.select_related('created_by', 'gym_branch').all()
        else:
            queryset = WorkoutPlan.objects.select_related('created_by', 'gym_branch').filter(
                gym_branch=user.gym_branch
            )

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = WorkoutPlanSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # POST - Create workout plan
    if user.role not in ['trainer', 'admin']:
        return error_response(message="Only trainers can create workout plans", code=403)

    serializer = WorkoutPlanCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return success_response(
            message="Workout plan created successfully",
            data=WorkoutPlanSerializer(serializer.instance).data,
            code=201
        )
    return error_response(message="Validation failed", errors=serializer.errors)


# ==================== Workout Tasks ====================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def workout_tasks(request):
    """
    GET: List workout tasks
        - Admin: All tasks
        - Manager: Tasks in their branch
        - Trainer: Tasks in their branch
        - Member: Only their own tasks
    POST: Create workout task (Trainer only)
    """
    user = request.user

    if request.method == 'GET':
        if user.role == 'admin':
            queryset = WorkoutTask.objects.select_related(
                'workout_plan', 'workout_plan__gym_branch', 'workout_plan__created_by', 'member'
            ).all()
        elif user.role == 'member':
            # Member can only see their own tasks
            queryset = WorkoutTask.objects.select_related(
                'workout_plan', 'workout_plan__gym_branch', 'workout_plan__created_by', 'member'
            ).filter(member=user)
        else:
            # Manager and Trainer see tasks in their branch
            queryset = WorkoutTask.objects.select_related(
                'workout_plan', 'workout_plan__gym_branch', 'workout_plan__created_by', 'member'
            ).filter(workout_plan__gym_branch=user.gym_branch)

        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = WorkoutTaskSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # POST - Create workout task
    if user.role not in ['trainer', 'admin']:
        return error_response(message="Only trainers can assign workout tasks", code=403)

    serializer = WorkoutTaskCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return success_response(
            message="Workout task assigned successfully",
            data=WorkoutTaskSerializer(serializer.instance).data,
            code=201
        )
    return error_response(message="Validation failed", errors=serializer.errors)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_task_status(request, task_id):
    """
    PATCH: Update task status
        - Admin: Can update any task
        - Trainer: Can update tasks in their branch
        - Member: Can only update their own tasks
    """
    user = request.user

    try:
        task = WorkoutTask.objects.select_related(
            'workout_plan', 'workout_plan__gym_branch', 'member'
        ).get(id=task_id)
    except WorkoutTask.DoesNotExist:
        return error_response(message="Task not found", errors={"task_id": ["Task not found"]}, code=404)

    # Permission checks
    if user.role == 'admin':
        pass  # Admin can update any task
    elif user.role == 'member':
        # Member can only update their own task
        if task.member != user:
            return error_response(message="You can only update your own tasks", code=403)
    elif user.role == 'trainer':
        # Trainer can only update tasks in their branch
        if task.workout_plan.gym_branch != user.gym_branch:
            return error_response(message="You can only update tasks in your branch", code=403)
    elif user.role == 'manager':
        # Manager can view but not update tasks (per requirements, only trainer and member can update)
        return error_response(message="Managers cannot update task status", code=403)
    else:
        return error_response(message="Permission denied", code=403)

    serializer = WorkoutTaskUpdateSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return success_response(
            message="Task status updated successfully",
            data=WorkoutTaskSerializer(task).data
        )
    return error_response(message="Validation failed", errors=serializer.errors)
