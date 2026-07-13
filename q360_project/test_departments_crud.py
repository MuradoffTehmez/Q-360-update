import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from apps.accounts.models import User
from apps.departments.models import Organization, Department
from django.urls import reverse

def main():
    print("--- Department CRUD Authenticated Test ---")
    admin_user = User.objects.filter(username='test_admin').first()
    if not admin_user:
        admin_user = User.objects.create_superuser('test_admin', 'admin@test.com', 'testpass123')
        
    client = Client()
    client.login(username='test_admin', password='testpass123')
    
    print("\n1. GET /departments/")
    res = client.get(reverse('departments:department-list'))
    print(f"Status: {res.status_code}")
    
    org, _ = Organization.objects.get_or_create(name='TestOrgCRUD', code='TOC1')
    
    print("\n2. POST /departments/create/")
    res = client.post(reverse('departments:department-create'), {
        'name': 'New CRUD Dept',
        'code': 'NCD-001',
        'organization': org.id,
        'description': 'Created via POST',
        'is_active': True
    })
    print(f"Status: {res.status_code} (Expect 302 redirect on success)")
    
    dept = Department.objects.filter(code='NCD-001').first()
    if dept:
        print(f"✅ DB verify: Department '{dept.name}' created successfully (ID: {dept.id})")
    else:
        print("❌ DB verify: Department not found!")
        return

    print("\n3. POST /departments/<id>/edit/")
    res = client.post(reverse('departments:department-update', args=[dept.pk]), {
        'name': 'Updated CRUD Dept',
        'code': 'NCD-001',
        'organization': org.id,
        'description': 'Updated via POST',
        'is_active': True
    })
    print(f"Status: {res.status_code}")
    
    dept.refresh_from_db()
    if dept.name == 'Updated CRUD Dept':
        print(f"✅ DB verify: Department name updated successfully to '{dept.name}'")
    else:
        print("❌ DB verify: Department name NOT updated!")

    print("\n4. POST /departments/<id>/delete/")
    res = client.post(reverse('departments:department-delete', args=[dept.pk]))
    print(f"Status: {res.status_code}")
    
    dept_exists = Department.objects.filter(code='NCD-001').exists()
    if not dept_exists:
        print("✅ DB verify: Department successfully deleted from DB!")
    else:
        print("❌ DB verify: Department STILL exists in DB!")

if __name__ == '__main__':
    main()
