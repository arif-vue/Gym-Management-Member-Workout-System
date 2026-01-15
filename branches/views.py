from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from .models import GymBranch
from .serializers import GymBranchSerializer
from authentications.permissions import IsAdmin


class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


def success_response(message, data=None, code=200):
    return Response({"success": True, "message": message, "data": data}, status=code)


def error_response(message, errors=None, code=400):
    return Response({"success": False, "message": message, "errors": errors or {}}, status=code)


@api_view(['GET', 'POST'])
@permission_classes([IsAdmin])
def gym_branches(request):
    """
    GET: List all gym branches (Admin only)
    POST: Create a new gym branch (Admin only)
    """
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
