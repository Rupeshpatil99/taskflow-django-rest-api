
from rest_framework.permissions import BasePermission, SAFE_METHODS

from projects.models import ProjectMembership


class IsProjectMember(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        membership = ProjectMembership.objects.filter(
            project=obj.project,
            user=request.user,
        ).first()

        if membership is None:
            return False

        # Managers can perform all task operations.
        if membership.role == ProjectMembership.Role.MANAGER:
            return True

        # Members can read tasks.
        if request.method in SAFE_METHODS:
            return True

        # Members may update only the status field.
        if request.method == "PATCH":
            return (
                bool(request.data)
                and set(request.data.keys()) == {"status"}
            )

        # Explicitly block DELETE, PUT, and other write methods.
        return False
