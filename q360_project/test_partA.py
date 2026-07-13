import requests
import re
import sys
import subprocess

session = requests.Session()
BASE_URL = "http://localhost:8000"

def run_db_check(code):
    cmd = f'docker compose exec web python manage.py shell -c "{code}"'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return res.stdout.strip()

print("=== 1. DEPARTMENT CRUD TEST ===")

# 1a. Login
print("a) Login with import_admin...")
login_page = session.get(f"{BASE_URL}/accounts/login/")
csrftoken = session.cookies.get('csrftoken')
login_data = {
    'username': 'import_admin',
    'password': 'testpass123',
    'csrfmiddlewaretoken': csrftoken
}
login_res = session.post(f"{BASE_URL}/accounts/login/", data=login_data, headers={'Referer': f"{BASE_URL}/accounts/login/"})
print(f"Login POST status: {login_res.status_code}")
print(f"Session cookies: {session.cookies.get_dict()}")

# 1b. GET departments list
print("\nb) GET /departments/")
dept_res = session.get(f"{BASE_URL}/departments/")
print(f"Status: {dept_res.status_code}")
if "Şöbələr" in dept_res.text:
    print("Success: 'Şöbələr' text found in HTML!")

# 1c. POST Create department
print("\nc) Create Department")
create_page = session.get(f"{BASE_URL}/departments/department/create/")
csrftoken = session.cookies.get('csrftoken')
org_id = run_db_check("from apps.departments.models import Organization; print(Organization.objects.first().id if Organization.objects.exists() else '')")
if not org_id:
    # Create an organization if none exists
    org_id = run_db_check("from apps.departments.models import Organization; org = Organization.objects.create(name='TestOrg', domain='test.com'); print(org.id)")

create_data = {
    'name': 'TestDepartmentReq',
    'code': 'TST01',
    'organization': org_id,
    'description': 'Test description',
    'csrfmiddlewaretoken': csrftoken
}
create_res = session.post(f"{BASE_URL}/departments/department/create/", data=create_data, headers={'Referer': f"{BASE_URL}/departments/department/create/"})
print(f"Create POST status: {create_res.status_code}")

# 1d. Verify DB
print("\nd) Verify in DB:")
exists = run_db_check("from apps.departments.models import Department; print(Department.objects.filter(name='TestDepartmentReq').exists())")
print(f"Department exists in DB? {exists}")

if exists == "True":
    dept_id = run_db_check("from apps.departments.models import Department; print(Department.objects.get(name='TestDepartmentReq').id)")
    
    # 1e. Edit
    print("\ne) Edit Department")
    edit_page = session.get(f"{BASE_URL}/departments/department/{dept_id}/update/")
    csrftoken = session.cookies.get('csrftoken')
    edit_data = {
        'name': 'TestDepartmentReq_Edited',
        'code': 'TST01_ED',
        'organization': org_id,
        'description': 'Edited description',
        'csrfmiddlewaretoken': csrftoken
    }
    edit_res = session.post(f"{BASE_URL}/departments/department/{dept_id}/update/", data=edit_data, headers={'Referer': f"{BASE_URL}/departments/department/{dept_id}/update/"})
    print(f"Edit POST status: {edit_res.status_code}")
    
    exists_edited = run_db_check("from apps.departments.models import Department; print(Department.objects.filter(name='TestDepartmentReq_Edited').exists())")
    print(f"Edited department exists in DB? {exists_edited}")
    
    # 1f. Delete
    print("\nf) Delete Department")
    del_page = session.get(f"{BASE_URL}/departments/department/{dept_id}/delete/")
    csrftoken = session.cookies.get('csrftoken')
    del_res = session.post(f"{BASE_URL}/departments/department/{dept_id}/delete/", data={'csrfmiddlewaretoken': csrftoken}, headers={'Referer': f"{BASE_URL}/departments/department/{dept_id}/delete/"})
    print(f"Delete POST status: {del_res.status_code}")
    
    exists_deleted = run_db_check("from apps.departments.models import Department; print(Department.objects.filter(name='TestDepartmentReq_Edited').exists())")
    print(f"Deleted department still in DB? {exists_deleted}")
else:
    print("Create failed. Finding form errors...")
    with open('error_form.html', 'w', encoding='utf-8') as f:
        f.write(create_res.text)
    print("Form HTML saved to error_form.html")

