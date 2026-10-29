
from django.db import transaction
from rest_framework import generics, permissions

from .models import Project, ProjectMembership
from .serializers import ProjectSerializer


class ProjectListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)

        ProjectMembership.objects.get_or_create(
            project=project,
            user=self.request.user,
            defaults={
                "role": ProjectMembership.Role.MANAGER,
            },
        )
