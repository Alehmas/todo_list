from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from tasks.models import Task
from .permissions import IsAuthorOrReadOnly
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on Task model.

    This viewset allows you to perform CRUD (Create, Retrieve, Update, Delete).

    Example Usage:
        To access all tasks:
        GET /tasks/

        To access all my tasks:
        GET /tasks/my/

        To retrieve a specific task:
        GET /tasks/{id}/

        To create a new task:
        POST /tasks/

        To completely update an existing task:
        PUT /tasks/{id}/

        To partially update an existing task:
        PATCH /tasks/{id}/

        To mark a task as completed:
        PATCH /tasks/{id}/completed

        To delete an existing task:
        DELETE /tasks/{id}/
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('status',)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user)

    @swagger_auto_schema(
            methods=['get'], operation_summary="My tasks",
            operation_description="Get a list of all user tasks.")
    @action(detail=False,)
    def my(self, request):
        """Get a list of all user tasks."""
        tasks = Task.objects.filter(user_id=request.user.id)
        status_contains = request.query_params.get('status')
        if status_contains:
            tasks = tasks.filter(status__icontains=status_contains)
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(tasks, request)
        serializer = self.get_serializer(page, many=True)
        data = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
            methods=['patch'], operation_summary="Task complete",
            operation_description="Set that the task has been completed.",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={}
            ),
            responses={200: TaskSerializer()}
    )
    @action(detail=True, methods=['patch'])
    def completed(self, request, pk=None):
        """Change the status of a specific user task to completed."""
        task = get_object_or_404(Task, pk=pk)
        if task.user_id != request.user:
            return Response('Forbiden! You are not the owner of this object',
                            status=status.HTTP_403_FORBIDDEN)
        if task.status == 'Completed':
            return Response('Already done!', status=status.HTTP_409_CONFLICT)
        task.status = 'Completed'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
