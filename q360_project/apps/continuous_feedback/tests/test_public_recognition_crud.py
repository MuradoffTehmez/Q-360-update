from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import User
from apps.continuous_feedback.models import PublicRecognition, QuickFeedback

class PublicRecognitionCRUDTests(APITestCase):
    def setUp(self):
        self.user_a = User.objects.create(username='user_a', role='employee')
        self.user_b = User.objects.create(username='user_b', role='employee')
        self.admin = User.objects.create(username='admin', is_superuser=True, is_staff=True, role='admin')
        
        self.feedback = QuickFeedback.objects.create(
            sender=self.user_a, 
            recipient=self.user_b, 
            feedback_type='recognition', 
            visibility='public', 
            message='Great job!'
        )
        self.recognition = PublicRecognition.objects.create(feedback=self.feedback)

    def test_create_recognition(self):
        feedback2 = QuickFeedback.objects.create(
            sender=self.user_a, 
            recipient=self.user_b, 
            feedback_type='recognition', 
            visibility='public', 
            message='Another one'
        )
        self.client.force_authenticate(user=self.user_a)
        response = self.client.post('/api/v1/continuous-feedback/public-recognition/', {
            'feedback': feedback2.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PublicRecognition.objects.filter(feedback=feedback2).exists())

    def test_update_recognition_sender(self):
        self.client.force_authenticate(user=self.user_a)
        response = self.client.patch(f'/api/v1/continuous-feedback/public-recognition/{self.recognition.id}/', {
            'is_featured': True
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recognition.refresh_from_db()
        self.assertTrue(self.recognition.is_featured)

    def test_update_recognition_unauthorized(self):
        self.client.force_authenticate(user=self.user_b)
        response = self.client.patch(f'/api/v1/continuous-feedback/public-recognition/{self.recognition.id}/', {
            'is_featured': True
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_recognition_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/v1/continuous-feedback/public-recognition/{self.recognition.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PublicRecognition.objects.filter(id=self.recognition.id).exists())

    def test_like_action(self):
        # Ensure existing custom action still works
        self.client.force_authenticate(user=self.user_b)
        response = self.client.post(f'/api/v1/continuous-feedback/public-recognition/{self.recognition.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('likes_count', 0), 1)
