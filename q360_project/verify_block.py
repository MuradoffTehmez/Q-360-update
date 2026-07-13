import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.test import Client
from apps.accounts.models import User
from apps.audit.models import BlockedIP

print("=== Starting IP Block/Unblock Verification ===")

# Create or get an admin user
admin_user, _ = User.objects.get_or_create(
    username='test_admin_verifier',
    email='verifier@example.com',
    defaults={'is_staff': True, 'is_superuser': True, 'role': 'admin'}
)
admin_user.set_password('pass123')
admin_user.save()

client = Client()
client.force_login(admin_user)

# Test Block IP
print("\n1. Testing Block IP API (/audit/api/block-ip/)")
response_block = client.post('/audit/api/block-ip/', {
    'ip_address': '192.168.1.99',
    'reason': 'Too many failed login attempts'
}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

print(f"HTTP Status: {response_block.status_code}")
print(f"Response JSON: {response_block.json()}")

# Verify DB
is_blocked = BlockedIP.objects.filter(ip_address='192.168.1.99').exists()
print(f"DB Query (Is 192.168.1.99 blocked?): {is_blocked}")

# Test Unblock IP
print("\n2. Testing Unblock IP API (/audit/api/unblock-ip/)")
response_unblock = client.post('/audit/api/unblock-ip/', {
    'ip_address': '192.168.1.99'
}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

print(f"HTTP Status: {response_unblock.status_code}")
print(f"Response JSON: {response_unblock.json()}")

# Verify DB
is_blocked_after = BlockedIP.objects.filter(ip_address='192.168.1.99').exists()
print(f"DB Query (Is 192.168.1.99 blocked?): {is_blocked_after}")

print("\n=== Verification Complete ===")
