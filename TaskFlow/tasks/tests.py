
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from projects.models import Project, ProjectMembership
from tasks.models import Task


User = get_user_model()


class TaskPermissionTests(APITestCase):
    def setUp(self):
        self.manager = User.objects.create_user(
            username="rupesh_test",
            password="TestPass123!",
        )
        self.member = User.objects.create_user(
            username="kartik_test",
            password="TestPass123!",
        )
        self.non_member = User.objects.create_user(
            username="outsider_test",
            password="TestPass123!",
        )

        self.project = Project.objects.create(
            name="TaskFlow Test Project",
            description="Project for API testing",
            owner=self.manager,
        )

        ProjectMembership.objects.create(
            project=self.project,
            user=self.manager,
            role=ProjectMembership.Role.MANAGER,
        )
        ProjectMembership.objects.create(
            project=self.project,
            user=self.member,
            role=ProjectMembership.Role.MEMBER,
        )

        self.task = Task.objects.create(
            project=self.project,
            title="Test Task",
            created_by=self.manager,
            status=Task.Status.TODO,
            priority=Task.Priority.MEDIUM,
        )

        self.list_url = reverse("task-list-create")
        self.detail_url = reverse(
            "task-detail",
            kwargs={"pk": self.task.pk},
        )

    
    def test_member_can_view_task(self):
        self.client.force_authenticate(user=self.member)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)


    def test_member_cannot_delete_task(self):
        self.client.force_authenticate(user=self.member)

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_manager_can_delete_task(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_non_member_cannot_view_task(self):
        self.client.force_authenticate(user=self.non_member)

        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
    
    def test_manager_can_create_task(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.post(
            self.list_url,
            {
                "project": self.project.id,
                "title": "New Automated Task",
                "description": "Created through API test",
                "priority": Task.Priority.HIGH,
                "status": Task.Status.TODO,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_member_cannot_create_task(self):
        self.client.force_authenticate(user=self.member)

        response = self.client.post(
            self.list_url,
            {
                "project": self.project.id,
                "title": "Member Task",
                "description": "Member should not create this",
                "priority": Task.Priority.MEDIUM,
                "status": Task.Status.TODO,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_member_can_update_task_status(self):
        self.client.force_authenticate(user=self.member)

        response = self.client.patch(
            self.detail_url,
            {"status": Task.Status.IN_PROGRESS},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.task.refresh_from_db()
        self.assertEqual(
            self.task.status,
            Task.Status.IN_PROGRESS,
        )
    
    def test_unauthenticated_user_cannot_list_tasks(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_unauthenticated_user_cannot_create_task(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(
            self.list_url,
            {
                "project": self.project.id,
                "title": "Unauthorized Task",
                "description": "This task should not be created",
                "priority": Task.Priority.HIGH,
                "status": Task.Status.TODO,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertFalse(
            Task.objects.filter(title="Unauthorized Task").exists()
        )
    
    def test_manager_can_update_task(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.patch(
            self.detail_url,
            {
                "title": "Updated TaskFlow Task",
                "priority": Task.Priority.HIGH,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.title,
            "Updated TaskFlow Task",
        )
        self.assertEqual(
            self.task.priority,
            Task.Priority.HIGH,
        )

    def test_member_cannot_update_task_title(self):
        self.client.force_authenticate(user=self.member)

        response = self.client.patch(
            self.detail_url,
            {"title": "Unauthorized Title Change"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.task.refresh_from_db()

        self.assertEqual(self.task.title, "Test Task")
    
    def test_task_creation_fails_without_title(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.post(
            self.list_url,
            {
                "project": self.project.id,
                "description": "Task without a title",
                "priority": Task.Priority.HIGH,
                "status": Task.Status.TODO,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(
            Task.objects.filter(
                project=self.project,
                description="Task without a title",
            ).exists()
        )
    
    def test_non_member_cannot_list_project_tasks(self):
        self.client.force_authenticate(user=self.non_member)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_manager_cannot_assign_task_to_non_member(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.post(
            self.list_url,
            {
                "project": self.project.id,
                "title": "Invalid Assignment Test",
                "description": "Assignee is outside the project",
                "assigned_to": self.non_member.id,
                "priority": Task.Priority.HIGH,
                "status": Task.Status.TODO,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(
            Task.objects.filter(
                title="Invalid Assignment Test"
            ).exists()
        )

    def test_task_creation_fails_without_title(self):
        self.client.force_authenticate(user=self.manager)

        response = self.client.post(
            self.list_url,
            {
                "project": self.project.id,
                "description": "Task without a title",
                "priority": Task.Priority.HIGH,
                "status": Task.Status.TODO,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(
            Task.objects.filter(
                project=self.project,
                description="Task without a title",
            ).exists()
        )
