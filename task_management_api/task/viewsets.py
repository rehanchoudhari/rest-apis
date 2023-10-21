from rest_framework import viewsets, mixins
from .serializers import TaskListSerializer
from .models import Task, TaskList, Attachment
from .permissions import IsAllowedToEditTaskListElseNone


class TaskListViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, 
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAllowedToEditTaskListElseNone, ]
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer