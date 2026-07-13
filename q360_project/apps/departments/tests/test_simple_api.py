from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from apps.accounts.models import User

class SimpleEndpointTest(APITestCase):
    def test_department_endpoint_unauthorized(self):
        url = '/api/v1/departments/departments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

