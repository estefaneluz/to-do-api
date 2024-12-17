from rest_framework import viewsets, permissions, status, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import TaskItem, TaskStatus, Tag
from .serializers import TaskItemSerializer, TagSerializer
from .pagination import CustomPagination
from users.models import User

class TaskItemViewSet(viewsets.ModelViewSet):
    serializer_class = TaskItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['tags']
    search_fields = ['title']

    def get_queryset(self):
        return TaskItem.objects.filter(created_by=self.request.user, is_active=True).order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['put'])
    def update_task(self, request, pk=None):
          task = self.get_object()
          title = request.data.get('title')
          tags = request.data.get('tags') 
          status = request.data.get('status')
          if status not in [TaskStatus.PENDING.name, TaskStatus.DONE.name]:
             return Response({'status': 'Invalid status'}, status=400)
          task.update_task(title, tags, TaskStatus[status])
          task.save()
          return Response(self.get_serializer(task).data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        task = self.get_object()
        task.deactivate()
        return Response(self.get_serializer(task).data)

    @action(detail=False, methods=['get'])
    def list_user_tasks(self, request):
        tasks = self.get_queryset()
        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def list_tags(self, request):
        tags = self.get_queryset()
        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data)

