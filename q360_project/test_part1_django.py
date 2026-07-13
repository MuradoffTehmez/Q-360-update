import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from apps.accounts.models import User
from apps.departments.models import Department, Organization

def main():
    print("=== A.1 DEPARTMENT CRUD TEST (AUTHENTICATED) ===")
    client = Client()
    
    # Ensure Organization exists
    org, _ = Organization.objects.get_or_create(name='TestOrg', code='TEST_ORG')
    
    # 1. Login
    print("\n1. Login with import_admin...")
    user = User.objects.get(username='import_admin')
    # Force login using client (simulates session cookie)
    client.force_login(user)
    print("Login successful. Session obtained.")
    
    # 2. GET /departments/
    print("\n2. GET /departments/...")
    res = client.get('/departments/')
    print(f"Status: {res.status_code}")
    if 'Şöbələr' in res.content.decode('utf-8'):
        print("Success: 'Şöbələr' found in response HTML!")
        
    # 3. Create Department
    print("\n3. POST /departments/department/create/...")
    create_data = {
        'name': 'TestDepartmentReq',
        'code': 'TST01',
        'organization': org.id,
        'description': 'Test description',
        'is_active': True
    }
    res = client.post('/departments/department/create/', data=create_data)
    print(f"Create POST status: {res.status_code}")
    if res.context and 'form' in res.context and res.context['form'].errors:
        print(f"Form errors: {res.context['form'].errors}")
        
    # 4. Verify in DB
    print("\n4. Verify in DB:")
    exists = Department.objects.filter(name='TestDepartmentReq').exists()
    print(f"Department created in DB? {exists}")
    
    if exists:
        dept = Department.objects.get(name='TestDepartmentReq')
        
        # 5. Edit Department
        print("\n5. POST /departments/department/{id}/update/...")
        edit_data = {
            'name': 'TestDepartmentReq_Edited',
            'code': 'TST01_ED',
            'organization': org.id,
            'description': 'Edited description',
            'is_active': True
        }
        res = client.post(f'/departments/department/{dept.id}/update/', data=edit_data)
        print(f"Edit POST status: {res.status_code}")
        if res.context and 'form' in res.context and res.context['form'].errors:
            print(f"Form errors: {res.context['form'].errors}")
            
        exists_edited = Department.objects.filter(name='TestDepartmentReq_Edited').exists()
        print(f"Edited department in DB? {exists_edited}")
        
        # 6. Delete Department
        print("\n6. POST /departments/department/{id}/delete/...")
        res = client.post(f'/departments/department/{dept.id}/delete/')
        print(f"Delete POST status: {res.status_code}")
        
        exists_deleted = Department.objects.filter(name='TestDepartmentReq_Edited').exists()
        print(f"Deleted department still in DB? {exists_deleted}")

if __name__ == '__main__':
    main()
