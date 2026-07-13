from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import User, Role

class RoleCRUDTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create(username='admin', is_superuser=True, is_staff=True, role='admin')
        self.admin.set_password('pass123')
        self.admin.save()
        
        self.employee = User.objects.create(username='employee', role='employee')
        self.employee.set_password('pass123')
        self.employee.save()
        
        # Add a custom role to choices dynamically for testing since Role.name has strict choices
        Role._meta.get_field('name').choices.append(('test_role', 'Test Role'))
        
        self.role = Role.objects.create(name='manager', display_name='Manager', description='MGR Role')

    def test_create_role_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/v1/accounts/roles/', {
            'name': 'test_role',
            'display_name': 'Test Role',
            'description': 'Test'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Role.objects.filter(name='test_role').exists())

    def test_update_role_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(f'/api/v1/accounts/roles/{self.role.id}/', {
            'name': 'manager',
            'display_name': 'Updated Manager',
            'description': 'Updated Description'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.role.refresh_from_db()
        self.assertEqual(self.role.display_name, 'Updated Manager')

    def test_delete_role_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(f'/api/v1/accounts/roles/{self.role.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Role.objects.filter(id=self.role.id).exists())

    def test_create_role_unauthorized(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.post('/api/v1/accounts/roles/', {
            'name': 'test_role',
            'display_name': 'Test Role',
            'description': 'Test'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_role_unauthorized(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.put(f'/api/v1/accounts/roles/{self.role.id}/', {
            'name': 'manager',
            'display_name': 'Hacked',
            'description': 'Hacked'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_role_unauthorized(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.delete(f'/api/v1/accounts/roles/{self.role.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
