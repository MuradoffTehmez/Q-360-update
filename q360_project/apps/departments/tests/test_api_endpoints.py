from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import User
from apps.departments.models import Department, Organization


class DepartmentAPIEndpointTests(APITestCase):
    """API endpoint tests for departments module."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123', email='test@example.com'
        )
        self.org = Organization.objects.create(name='Test Org', code='TO')
        self.dept = Department.objects.create(
            name='IT Department', code='IT', organization=self.org
        )
        self.list_url = '/api/v1/departments/departments/'
        self.detail_url = f'/api/v1/departments/departments/{self.dept.pk}/'

    def test_get_departments_authenticated(self):
        """Authenticated GET list → 200"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_departments_unauthorized(self):
        """Unauthenticated GET list → 401"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_department_not_found(self):
        """GET nonexistent detail → 404"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/departments/departments/999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
