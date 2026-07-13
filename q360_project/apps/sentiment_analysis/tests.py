from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import User
from apps.sentiment_analysis.models import SentimentFeedback


class SentimentAPIEndpointTests(APITestCase):
    """API endpoint tests for sentiment_analysis module."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123', email='test@example.com'
        )
        self.feedback = SentimentFeedback.objects.create(
            user=self.user, feedback_text='Good environment', sentiment_label='positive', sentiment_score=0.8, confidence=0.9
        )
        self.list_url = '/api/v1/sentiment/feedback/'
        self.detail_url = f'/api/v1/sentiment/feedback/{self.feedback.pk}/'

    def test_get_feedback_authenticated(self):
        """Authenticated GET list → 200"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_feedback_unauthorized(self):
        """Unauthenticated GET list → 401"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_feedback_not_found(self):
        """GET nonexistent detail → 404"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/sentiment/feedback/999999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
