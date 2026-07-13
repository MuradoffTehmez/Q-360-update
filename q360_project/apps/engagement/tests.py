from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import User
from apps.engagement.models import PulseSurvey


class EngagementAPIEndpointTests(APITestCase):
    """API endpoint tests for engagement module."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123', email='test@example.com'
        )
        self.survey = PulseSurvey.objects.create(
            title='Test Survey', created_by=self.user, status='active', start_date='2024-01-01T00:00:00Z', end_date='2024-12-31T00:00:00Z'
        )
        self.list_url = '/api/v1/engagement/pulse-surveys/'
        self.detail_url = f'/api/v1/engagement/pulse-surveys/{self.survey.pk}/'

    def test_get_pulse_surveys_authenticated(self):
        """Authenticated GET list → 200"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_pulse_surveys_unauthorized(self):
        """Unauthenticated GET list → 401"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_pulse_survey_not_found(self):
        """GET nonexistent detail → 404"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/engagement/pulse-surveys/999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
