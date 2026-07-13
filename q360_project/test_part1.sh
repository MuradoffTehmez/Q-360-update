#!/bin/bash
set -e

echo "=== A.1 DEPARTMENT CRUD TEST ==="

echo "1. Login and get cookies..."
# First GET to capture CSRF token
curl -s -c cookies.txt http://localhost:8000/accounts/login/ > /dev/null
CSRF=$(grep csrftoken cookies.txt | awk '{print $7}')

# POST to login
curl -s -c cookies.txt -b cookies.txt -d "username=import_admin&password=testpass123&csrfmiddlewaretoken=$CSRF" -X POST http://localhost:8000/accounts/login/ > /dev/null
echo "Login completed."

echo -e "\n2. GET /departments/"
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -b cookies.txt http://localhost:8000/departments/)
echo "Status: $HTTP_STATUS"
curl -s -b cookies.txt http://localhost:8000/departments/ | grep -iE "<title>|Şöbələr" | head -n 3

echo -e "\n3. POST /departments/create/ to create a new department"
# GET to capture CSRF token for the create form
curl -s -c cookies.txt -b cookies.txt http://localhost:8000/departments/create/ > /dev/null
CSRF=$(grep csrftoken cookies.txt | awk '{print $7}')

# POST to create
curl -s -c cookies.txt -b cookies.txt -d "name=TestDepartmentPart1&description=TestDesc&csrfmiddlewaretoken=$CSRF" -X POST http://localhost:8000/departments/create/ > /dev/null
echo "Creation POST completed."

echo -e "\n4. Verify in DB:"
python manage.py shell -c "from apps.departments.models import Department; print('Department created in DB:', Department.objects.filter(name='TestDepartmentPart1').exists())"

echo -e "\n5. Edit the department via POST"
# Get the ID of the new department
DEPT_ID=$(python manage.py shell -c "from apps.departments.models import Department; dept = Department.objects.filter(name='TestDepartmentPart1').first(); print(dept.id if dept else '')")

# GET to capture CSRF token for the edit form
curl -s -c cookies.txt -b cookies.txt http://localhost:8000/departments/${DEPT_ID}/update/ > /dev/null
CSRF=$(grep csrftoken cookies.txt | awk '{print $7}')

# POST to edit
curl -s -c cookies.txt -b cookies.txt -d "name=TestDepartmentEdited&description=EditedDesc&csrfmiddlewaretoken=$CSRF" -X POST http://localhost:8000/departments/${DEPT_ID}/update/ > /dev/null
echo "Edit POST completed."
python manage.py shell -c "from apps.departments.models import Department; print('Department edited in DB:', Department.objects.filter(name='TestDepartmentEdited').exists())"

echo -e "\n6. Delete the department via POST"
# GET to capture CSRF token for the delete form
curl -s -c cookies.txt -b cookies.txt http://localhost:8000/departments/${DEPT_ID}/delete/ > /dev/null
CSRF=$(grep csrftoken cookies.txt | awk '{print $7}')

# POST to delete
curl -s -c cookies.txt -b cookies.txt -d "csrfmiddlewaretoken=$CSRF" -X POST http://localhost:8000/departments/${DEPT_ID}/delete/ > /dev/null
echo "Delete POST completed."
python manage.py shell -c "from apps.departments.models import Department; print('Department still in DB:', Department.objects.filter(name='TestDepartmentEdited').exists())"

echo "=== DONE A.1 ==="
