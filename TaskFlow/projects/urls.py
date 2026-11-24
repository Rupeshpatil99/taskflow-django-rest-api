
from django.urls import path

from .views import (
    ProjectListCreateAPIView,
    ProjectMemberListCreateAPIView,
    ProjectMemberDeleteAPIView,
)

urlpatterns = [
    path(
        "",
        ProjectListCreateAPIView.as_view(),
        name="project-list-create",
    ),
    path(
        "<int:project_id>/members/",
        ProjectMemberListCreateAPIView.as_view(),
        name="project-member-list-create",
    ),
    path(
        "<int:project_id>/members/<int:user_id>/",
        ProjectMemberDeleteAPIView.as_view(),
        name="project-member-delete",
    ),
]
