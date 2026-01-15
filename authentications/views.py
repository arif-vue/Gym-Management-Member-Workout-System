from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import CustomUser, GymBranch
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    LoginSerializer,
    GymBranchSerializer,
)
from .permissions import IsAdmin, IsAdminOrManager

User = get_user_model()


def success_response(message, data=None, code=200):
    return Response({"success": True, "message": message, "data": data}, status=code)


def error_response(message, errors=None, code=400):
    return Response({"success": False, "message": message, "errors": errors or {}}, status=code)


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ==================== Authentication ====================

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        user_serializer = UserSerializer(user)
        return Response({
            "success": True,
            "message": "Login successful",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "data": user_serializer.data
        }, status=status.HTTP_200_OK)
    return error_response(message="Invalid credentials", errors=serializer.errors, code=401)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    token = request.data.get('refresh_token')
    if not token:
        return error_response(message="Refresh token is required", errors={"refresh_token": ["This field is required"]})
    try:
        refresh = RefreshToken(token)
        return success_response(
            message="Token refreshed successfully",
            data={"access_token": str(refresh.access_token), "refresh_token": str(refresh)}
        )
    except Exception as e:
        return error_response(message="Invalid refresh token", errors={"token": [str(e)]}, code=401)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    serializer = UserSerializer(request.user)
    return success_response(message="Profile retrieved successfully", data=serializer.data)


# ==================== Gym Branch Management (Admin Only) ====================

@api_view(['GET', 'POST'])
@permission_classes([IsAdmin])
def gym_branches(request):
    if request.method == 'GET':
        branches = GymBranch.objects.all()
        paginator = StandardPagination()
        page = paginator.paginate_queryset(branches, request)
        serializer = GymBranchSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    serializer = GymBranchSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return success_response(message="Gym branch created successfully", data=serializer.data, code=201)
    return error_response(message="Validation failed", errors=serializer.errors)


# ==================== User Management ====================

@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrManager])
def users(request):
    if request.method == 'GET':
        user = request.user
        if user.role == 'admin':
            queryset = User.objects.select_related('gym_branch').all()
        else:
            # Manager can only see users in their branch
            queryset = User.objects.select_related('gym_branch').filter(gym_branch=user.gym_branch)
        
        paginator = StandardPagination()
        page = paginator.paginate_queryset(queryset, request)
        serializer = UserSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    # POST - Create user
    serializer = UserCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return success_response(message="User created successfully", data=UserSerializer(serializer.instance).data, code=201)
    return error_response(message="Validation failed", errors=serializer.errors)
