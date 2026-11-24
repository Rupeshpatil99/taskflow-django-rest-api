
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Project, ProjectMembership
from .serializers import ProjectSerializer, ProjectMemberSerializer


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


class ProjectMemberListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_project(self):
        return get_object_or_404(
            Project,
            pk=self.kwargs["project_id"],
        )

    def check_project_permission(self):
        project = self.get_project()

        membership = ProjectMembership.objects.filter(
            project=project,
            user=self.request.user,
        ).first()

        is_owner = project.owner_id == self.request.user.id
        is_manager = (
            membership is not None
            and membership.role == ProjectMembership.Role.MANAGER
        )

        if self.request.method == "POST":
            if not (is_owner or is_manager):
                raise PermissionDenied(
                    "Only project managers can add members."
                )
        elif not (is_owner or membership is not None):
            raise PermissionDenied(
                "You are not a member of this project."
            )

        return project

    def get_queryset(self):
        project = self.check_project_permission()

        return ProjectMembership.objects.filter(
            project=project
        ).select_related("user")

    def perform_create(self, serializer):
        project = self.check_project_permission()

        serializer.save(
            project=project,
            role=ProjectMembership.Role.MEMBER,
        )

class ProjectMemberDeleteAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProjectMemberSerializer

    def get_object(self):
        project = get_object_or_404(
            Project,
            pk=self.kwargs["project_id"],
        )

        membership = ProjectMembership.objects.filter(
            project=project,
            user=self.request.user,
        ).first()

        is_owner = project.owner_id == self.request.user.id
        is_manager = (
            membership is not None
            and membership.role == ProjectMembership.Role.MANAGER
        )

        if not (is_owner or is_manager):
            raise PermissionDenied(
                "Only project managers can remove members."
            )

        member = get_object_or_404(
            ProjectMembership,
            project=project,
            user_id=self.kwargs["user_id"],
        )

        if member.user_id == project.owner_id:
            raise PermissionDenied(
                "Project owner cannot be removed."
            )

        return member
