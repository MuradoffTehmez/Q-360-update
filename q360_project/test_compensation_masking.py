import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from apps.accounts.models import User
from apps.compensation.models import SalaryInformation
from apps.departments.models import Department, Organization
from decimal import Decimal
from django.urls import reverse

def main():
    print("Creating users for testing...")
    admin_user, _ = User.objects.get_or_create(email='test_admin@example.com', defaults={
        'username': 'test_admin',
        'first_name': 'Test',
        'last_name': 'Admin',
        'role': 'admin'
    })
    admin_user.set_password('testpass123')
    admin_user.save()

    hr_user, _ = User.objects.get_or_create(email='test_hr@example.com', defaults={
        'username': 'test_hr',
        'first_name': 'Test',
        'last_name': 'HR',
        'role': 'hr'
    })
    hr_user.set_password('testpass123')
    hr_user.save()

    employee_user, _ = User.objects.get_or_create(email='test_emp@example.com', defaults={
        'username': 'test_emp',
        'first_name': 'Test',
        'last_name': 'Employee',
        'role': 'employee'
    })
    employee_user.set_password('testpass123')
    employee_user.save()

    manager_user, _ = User.objects.get_or_create(email='test_mgr@example.com', defaults={
        'username': 'test_mgr',
        'first_name': 'Test',
        'last_name': 'Manager',
        'role': 'employee'  # Role is employee, but will be head of department
    })
    manager_user.set_password('testpass123')
    manager_user.save()

    # Make manager_user a manager
    org, _ = Organization.objects.get_or_create(name="Test Org", code="ORG1")
    dept, _ = Department.objects.get_or_create(name="Test Dept", code="DEPT1", organization=org, defaults={'head': manager_user})
    if dept.head != manager_user:
        dept.head = manager_user
        dept.save()

    employee_user.department = dept
    employee_user.save()

    # Create salary info for employee
    SalaryInformation.objects.update_or_create(user=employee_user, defaults={
        'base_salary': Decimal('2500.00'),
        'currency': 'AZN',
        'payment_frequency': 'monthly',
        'effective_date': '2023-01-01'
    })

    client = Client()
    
    print("--- Testing Own Dashboard View with Employee (Should see own salary) ---")
    client.login(username='test_emp', password='testpass123')
    res = client.get(reverse('compensation:dashboard'))
    print("Employee Dashboard Status:", res.status_code)
    content = res.content.decode('utf-8')
    if "2500" in content:
        print("✅ Employee sees own 2500 AZN")
    else:
        print("❌ Error: Employee cannot see own salary! (Status {})".format(res.status_code))
        with open('emp_dash.html', 'w', encoding='utf-8') as f:
            f.write(content)

    print("--- Testing Manager View with Manager User (Should see masked) ---")
    client.login(username='test_mgr', password='testpass123')
    res = client.get(reverse('compensation:salary_list'))
    print("Manager List Status:", res.status_code)
    content = res.content.decode('utf-8')
    if "2500" in content:
        print("❌ Error: Manager sees real salary of employee!")
    elif "***" in content:
        print("✅ Manager successfully sees masked salary (***)")
    else:
        print("❓ Manager view result unclear. Could not find *** or 2500")
        with open('mgr_list.html', 'w', encoding='utf-8') as f:
            f.write(content)

    print("--- Testing Manager View with HR (Should see real salary) ---")
    client.login(username='test_hr', password='testpass123')
    res = client.get(reverse('compensation:salary_list'))
    print("HR List Status:", res.status_code)
    content = res.content.decode('utf-8')
    if "2500" in content:
        print("✅ HR successfully sees real salary 2500 AZN")
    else:
        print("❌ Error: HR cannot see real salary!")
        with open('hr_list.html', 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    main()
