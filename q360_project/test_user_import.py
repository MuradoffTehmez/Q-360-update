import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


from django.test import Client
from apps.accounts.models import User
from django.urls import reverse

def main():
    print("--- Bulk User Import Authenticated Test ---")
    admin_user = User.objects.filter(username='import_admin').first()
    if not admin_user:
        admin_user = User.objects.create_superuser('import_admin', 'import_admin@example.com', 'testpass123')
        
    # Clean up previous users
    User.objects.filter(email__startswith='valid').delete()
    User.objects.filter(first_name='Invalid').delete()
    User.objects.filter(first_name='Missing').delete()

    # Create test CSV
    csv_content = """first_name,last_name,email,role,department,position
Valid,One,valid1@example.com,employee,IT,Developer
Valid,Two,valid2@example.com,manager,HR,Manager
Invalid,Email,invalid-email,employee,IT,Tester
Missing,Role,missing_role@example.com,,IT,Support
Valid,Three,valid3@example.com,hr,HR,Specialist
"""
    with open('test_import.csv', 'w', encoding='utf-8') as f:
        f.write(csv_content)

    client = Client()
    client.login(username='import_admin', password='testpass123')
    
    print("\n1. POST /accounts/users/import/")
    with open('test_import.csv', 'rb') as f:
        res = client.post(reverse('accounts:user-import'), {'import_file': f})
        
    print(f"Status: {res.status_code}")
    if res.status_code == 200:
        with open('import_res.html', 'w', encoding='utf-8') as f:
            f.write(res.content.decode('utf-8'))
        print("Response saved to import_res.html")
    
    print("Waiting 5 seconds for Celery task to finish...")
    time.sleep(5)
    
    # Check DB
    print("\n2. DB Verification:")
    valid1 = User.objects.filter(email='valid1@example.com').exists()
    valid2 = User.objects.filter(email='valid2@example.com').exists()
    valid3 = User.objects.filter(email='valid3@example.com').exists()
    invalid1 = User.objects.filter(first_name='Invalid').exists()
    invalid2 = User.objects.filter(first_name='Missing').exists()
    
    print(f"Valid One created: {valid1}")
    print(f"Valid Two created: {valid2}")
    print(f"Valid Three created: {valid3}")
    print(f"Invalid Email created (should be False): {invalid1}")
    print(f"Missing Role created (should be False): {invalid2}")
    
    if valid1 and valid2 and valid3 and not invalid1 and not invalid2:
        print("✅ DB verify: Import logic works correctly!")
    else:
        print("❌ DB verify: Import logic failed!")

if __name__ == '__main__':
    main()
