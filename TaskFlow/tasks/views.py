
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsProjectMember
from projects.models import ProjectMembership
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "status",
        "priority",
        "project",
        "assigned_to",
    ]

    search_fields = ["title", "description"]

    ordering_fields = [
        "created_at",
        "due_date",
        "priority",
        "status",
    ]

    ordering = ["-created_at"]


    def get_queryset(self):
        return Task.objects.filter(
            project__memberships__user=self.request.user
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]

        membership = project.memberships.filter(
            user=self.request.user
        ).first()

        if not membership:
            raise ValidationError({
                "project": "You must belong to this project."
            })

        if membership.role != ProjectMembership.Role.MANAGER:
            raise ValidationError({
                "detail": "Only project managers can create tasks."
            })

        assigned_to = serializer.validated_data.get("assigned_to")

        if assigned_to and not project.memberships.filter(
            user=assigned_to
        ).exists():
            raise ValidationError({
                "assigned_to": "The assignee must belong to this project."
            })

        serializer.save(created_by=self.request.user)


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsProjectMember,
    ]

    def get_queryset(self):
        return Task.objects.filter(
            project__memberships__user=self.request.user
        ).distinct()

    def perform_update(self, serializer):
        task = self.get_object()

        assigned_to = serializer.validated_data.get(
            "assigned_to",
            task.assigned_to,
        )

        if assigned_to and not task.project.memberships.filter(
            user=assigned_to
        ).exists():
            raise ValidationError({
                "assigned_to": "The assignee must belong to this project."
            })

        serializer.save()
