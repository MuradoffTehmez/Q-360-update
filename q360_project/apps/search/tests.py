from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import User


class SearchAPIEndpointTests(APITestCase):
    """API endpoint tests for search module."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123', email='test@example.com'
        )
        self.search_url = '/api/v1/search/'

    def test_get_search_authenticated(self):
        """Authenticated GET list → 200"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.search_url, {'q': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_search_unauthorized(self):
        """Unauthenticated GET list → 401"""
        response = self.client.get(self.search_url, {'q': 'test'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_search_invalid_query(self):
        """GET with short query → 400"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.search_url, {'q': 't'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
