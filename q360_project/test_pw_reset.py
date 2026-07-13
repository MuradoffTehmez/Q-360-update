import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def main():
    print("--- Trigger Password Reset ---")
    client = Client()
    
    # POST to password reset
    res = client.post(reverse('accounts:password-reset'), {
        'email': 'import_admin@example.com'
    })
    
    print(f"Status: {res.status_code}")

if __name__ == '__main__':
    main()
