import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from apps.accounts.models import User

def run_tests():
    print("=== TƏHLÜKƏSİZLİK YOXLAMASI BAŞLAYIR ===")
    
    # 1. Create a regular user and a superuser for testing
    try:
        regular_user, created = User.objects.get_or_create(
            username='test_regular', 
            defaults={'email': 'regular@example.com'}
        )
        if created:
            regular_user.set_password('TestPass123')
            regular_user.is_superuser = False
            regular_user.is_staff = False
            regular_user.save()
            
        super_user, created = User.objects.get_or_create(
            username='test_super', 
            defaults={'email': 'super@example.com'}
        )
        if created:
            super_user.set_password('TestPass123')
            super_user.is_superuser = True
            super_user.is_staff = True
            super_user.save()
    except Exception as e:
        print(f"Failed to create test users: {e}")
        sys.exit(1)

    urls_to_test = [
        # Workflow Engine
        '/workflow/dashboard/',
        '/workflow/workflows/',
        '/workflow/designer/',
        '/workflow/versions/',
        '/workflow/history/',
        '/workflow/logs/',
        '/workflow/monitoring/',
        # Approval Engine
        '/approval/dashboard/',
        '/approval/rules/',
        '/approval/chains/',
        '/approval/history/',
        '/approval/queue/',
        '/approval/delegations/',
        # Access Control
        '/access-control/dashboard/',
        '/access-control/roles/',
        '/access-control/permissions/',
        '/access-control/policies/',
        '/access-control/groups/',
        '/access-control/access-requests/',
        '/access-control/access-history/',
        # Policy Engine
        '/policy-engine/dashboard/',
        '/policy-engine/policies/',
        '/policy-engine/rules/',
        '/policy-engine/simulator/',
        '/policy-engine/versions/',
        '/policy-engine/logs/',
        # Feature Flags
        '/feature-flags/dashboard/',
        '/feature-flags/flags/',
        '/feature-flags/environments/',
        '/feature-flags/rollouts/',
        '/feature-flags/experiments/',
        '/feature-flags/history/',
    ]

    client = Client()

    # Test as regular user
    print("\n--- ADİ İSTİFADƏÇİ (SUPERUSER OLMAYAN) TESTİ ---")
    client.force_login(regular_user)
    regular_passed = True
    for url in urls_to_test:
        response = client.get(url)
        status = response.status_code
        if status == 403:
            print(f"SUCCESS: {url} qaytardı 403")
        elif status == 302 and 'login' in response.url.lower():
            # Sometimes user_passes_test returns 302 if permission_denied isn't raised
            print(f"SUCCESS (Redirect): {url} qaytardı {status} -> {response.url}")
        else:
            print(f"FAIL: {url} qaytardı {status}")
            regular_passed = False

    # Test as superuser
    print("\n--- SUPERUSER TESTİ ---")
    client.force_login(super_user)
    super_passed = True
    for url in urls_to_test:
        response = client.get(url)
        status = response.status_code
        if status == 200:
            print(f"SUCCESS: {url} qaytardı 200")
        else:
            print(f"FAIL: {url} qaytardı {status}")
            super_passed = False

    print("\n=== YEKUN NƏTİCƏ ===")
    if regular_passed and super_passed:
        print("✅ BÜTÜN TESTLƏR UĞURLA KEÇDİ!")
    else:
        print("❌ TESTLƏRDƏ XƏTA VAR!")
        
if __name__ == "__main__":
    run_tests()
