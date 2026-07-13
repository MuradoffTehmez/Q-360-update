import subprocess
import os
import re

def run_cmd(cmd):
    print(f"> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip()[:500] + ('...' if len(result.stdout) > 500 else ''))
    if result.stderr:
        print(result.stderr.strip())
    return result.stdout

def main():
    print("=== A.1 DEPARTMENT CRUD TEST ===")
    
    # 1. Get CSRF Token
    print("1. Login and get cookies...")
    run_cmd('curl.exe -s -c cookies.txt http://localhost:8000/accounts/login/')
    
    # Extract CSRF token
    csrf_token = ""
    with open('cookies.txt', 'r') as f:
        for line in f:
            if 'csrftoken' in line:
                csrf_token = line.strip().split('\t')[-1]
                break
                
    print(f"Got CSRF token: {csrf_token}")
    
    # POST login
    run_cmd(f'curl.exe -s -c cookies.txt -b cookies.txt -d "username=import_admin&password=testpass123&csrfmiddlewaretoken={csrf_token}" -X POST http://localhost:8000/accounts/login/')
    print("Login completed.")
    
    # 2. Get Departments
    print("\n2. GET /departments/")
    out = run_cmd('curl.exe -s -I -b cookies.txt http://localhost:8000/departments/')
    
    out_html = run_cmd('curl.exe -s -b cookies.txt http://localhost:8000/departments/')
    
    # 3. Create Department via POST
    print("\n3. POST /departments/create/")
    run_cmd('curl.exe -s -c cookies.txt -b cookies.txt http://localhost:8000/departments/create/')
    with open('cookies.txt', 'r') as f:
        for line in f:
            if 'csrftoken' in line:
                csrf_token = line.strip().split('\t')[-1]
                
    run_cmd(f'curl.exe -s -c cookies.txt -b cookies.txt -d "name=TestDepartmentPart1&description=TestDesc&csrfmiddlewaretoken={csrf_token}" -X POST http://localhost:8000/departments/create/')
    
    # 4. Verify in DB
    print("\n4. Verify in DB:")
    run_cmd('docker compose exec web python manage.py shell -c "from apps.departments.models import Department; print(\'Exists:\', Department.objects.filter(name=\'TestDepartmentPart1\').exists())"')
    
    # 5. Edit Department
    print("\n5. Edit the department")
    dept_id_out = run_cmd('docker compose exec web python manage.py shell -c "from apps.departments.models import Department; dept = Department.objects.filter(name=\'TestDepartmentPart1\').first(); print(dept.id if dept else \'\')"')
    dept_id = dept_id_out.strip()
    
    run_cmd(f'curl.exe -s -c cookies.txt -b cookies.txt http://localhost:8000/departments/{dept_id}/update/')
    with open('cookies.txt', 'r') as f:
        for line in f:
            if 'csrftoken' in line:
                csrf_token = line.strip().split('\t')[-1]
                
    run_cmd(f'curl.exe -s -c cookies.txt -b cookies.txt -d "name=TestDepartmentEdited&description=EditedDesc&csrfmiddlewaretoken={csrf_token}" -X POST http://localhost:8000/departments/{dept_id}/update/')
    run_cmd('docker compose exec web python manage.py shell -c "from apps.departments.models import Department; print(\'Edited Exists:\', Department.objects.filter(name=\'TestDepartmentEdited\').exists())"')
    
    # 6. Delete Department
    print("\n6. Delete the department")
    run_cmd(f'curl.exe -s -c cookies.txt -b cookies.txt http://localhost:8000/departments/{dept_id}/delete/')
    with open('cookies.txt', 'r') as f:
        for line in f:
            if 'csrftoken' in line:
                csrf_token = line.strip().split('\t')[-1]
                
    run_cmd(f'curl.exe -s -c cookies.txt -b cookies.txt -d "csrfmiddlewaretoken={csrf_token}" -X POST http://localhost:8000/departments/{dept_id}/delete/')
    run_cmd('docker compose exec web python manage.py shell -c "from apps.departments.models import Department; print(\'Deleted Exists:\', Department.objects.filter(name=\'TestDepartmentEdited\').exists())"')
    
    print("\n=== DONE A.1 ===")

if __name__ == '__main__':
    main()
