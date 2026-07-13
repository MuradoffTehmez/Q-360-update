from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import User
from apps.notifications.models import NotificationMethod


class NotificationAPIEndpointTests(APITestCase):
    """API endpoint tests for notifications module."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123', email='test@example.com'
        )
        self.method = NotificationMethod.objects.create(
            name='Email', method_type='email', is_active=True
        )
        self.list_url = '/api/v1/notifications/methods/'
        self.detail_url = f'/api/v1/notifications/methods/{self.method.pk}/'

    def test_get_methods_authenticated(self):
        """Authenticated GET list → 200"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_methods_unauthorized(self):
        """Unauthenticated GET list → 401"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_method_not_found(self):
        """GET nonexistent detail → 404"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/notifications/methods/999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
