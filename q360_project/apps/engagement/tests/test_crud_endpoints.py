from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import User
from apps.engagement.models import GamificationBadge, UserBadge
from django.utils import timezone

class BadgeCRUDTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(username='admin', is_superuser=True, is_staff=True, role='admin')
        self.admin.set_password('pass123')
        self.admin.save()
        
        self.user = User.objects.create(username='user', role='employee')
        self.user.set_password('pass123')
        self.user.save()
        
        self.badge = GamificationBadge.objects.create(
            name='Test Badge', description='Test', category='performance', icon='star'
        )

    def test_create_badge_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/v1/engagement/badges/', {
            'name': 'New Badge',
            'description': 'Test',
            'category': 'learning',
            'icon': 'book'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_badge_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(f'/api/v1/engagement/badges/{self.badge.id}/', {
            'name': 'Updated Badge',
            'description': 'Test',
            'category': 'learning',
            'icon': 'book'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_badge_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/v1/engagement/badges/{self.badge.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_badge_unauthorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/engagement/badges/', {
            'name': 'Hacked Badge'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserBadgeCRUDTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(username='admin2', is_superuser=True, is_staff=True, role='admin')
        self.user = User.objects.create(username='user2', role='employee')
        self.badge = GamificationBadge.objects.create(name='Test Badge 2', category='performance')
        self.user_badge = UserBadge.objects.create(user=self.user, badge=self.badge)

    def test_create_user_badge_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/v1/engagement/user-badges/', {
            'user_id': self.user.id,
            'badge_id': self.badge.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_user_badge_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/v1/engagement/user-badges/{self.user_badge.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_user_badge_unauthorized(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/engagement/user-badges/', {
            'user_id': self.user.id,
            'badge_id': self.badge.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
