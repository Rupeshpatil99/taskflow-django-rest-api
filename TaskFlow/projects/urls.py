from django.urls import path
from .views import ProjectListCreateAPIView

urlpatterns = [
    path("", ProjectListCreateAPIView.as_view(), name="project-list-create"),
]