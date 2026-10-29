
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from projects.models import Project, ProjectMembership
from projects.models import Project

User = get_user_model()


class ProjectAPITests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username="project_owner",
            password="TestPass123!",
        )

        self.other_user = User.objects.create_user(
            username="other_user",
            password="TestPass123!",
        )

        self.project = Project.objects.create(
            name="Owner Project",
            description="Project owned by test user",
            owner=self.owner,
        )

        self.url = reverse("project-list-create")

    def test_user_can_list_own_projects(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(
            response.data["results"][0]["name"],
            "Owner Project",
        )

    def test_user_cannot_see_other_users_projects(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(response.data["count"], 0)

    def test_created_project_belongs_to_logged_in_user(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.url,
            {
                "name": "New Project",
                "description": "Created through API testing",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        project = Project.objects.get(name="New Project")

        self.assertEqual(project.owner, self.owner)
    
    def test_project_owner_becomes_manager_automatically(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.url,
            {
                "name": "Membership Test Project",
                "description": "Testing automatic membership",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        project = Project.objects.get(
            name="Membership Test Project"
        )

        membership = ProjectMembership.objects.get(
            project=project,
            user=self.owner,
        )

        self.assertEqual(
            membership.role,
            ProjectMembership.Role.MANAGER,
        )
    
    def test_project_owner_membership_is_created_once(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.url,
            {
                "name": "Unique Membership Project",
                "description": "Testing membership uniqueness",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        project = Project.objects.get(
            name="Unique Membership Project"
        )

        memberships = ProjectMembership.objects.filter(
            project=project,
            user=self.owner,
        )

        self.assertEqual(memberships.count(), 1)
        self.assertEqual(
            memberships.first().role,
            ProjectMembership.Role.MANAGER,
        )
