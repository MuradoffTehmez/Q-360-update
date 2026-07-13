from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from apps.accounts.models import User
from apps.leave_attendance.models import LeaveType, LeaveRequest
from datetime import date, timedelta
from decimal import Decimal

class LeaveAPIEndpointTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
        self.leave_type = LeaveType.objects.create(name='Annual', code='ANN', days_per_year=20)
        self.leave_url = '/api/v1/leave-attendance/leave-requests/'
        
    def test_get_leave_requests_unauthorized(self):
        response = self.client.get(self.leave_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_leave_requests_authorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.leave_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        
    def test_create_leave_request(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'leave_type': self.leave_type.id,
            'start_date': str(date.today()),
            'end_date': str(date.today() + timedelta(days=2)),
            'reason': 'Vacation'
        }
        response = self.client.post(self.leave_url, data, format='json')
        if response.status_code == 400:
            print("ERROR RESPONSE:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_get_invalid_leave_request(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'{self.leave_url}99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
