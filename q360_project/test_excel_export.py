import os
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from apps.accounts.models import User
from django.urls import reverse

def main():
    print("--- Excel Export Authenticated Test ---")
    admin_user = User.objects.filter(username='import_admin').first()
    
    client = Client()
    client.login(username='import_admin', password='testpass123')
    
    print("\n1. GET /accounts/users/export/")
    res = client.get(reverse('accounts:user-export'))
    print(f"Status: {res.status_code}")
    
    content_type = res.get('Content-Type')
    print(f"Content-Type: {content_type}")
    
    if res.status_code == 200 and 'spreadsheetml' in content_type:
        print("✅ Correct Content-Type for Excel (.xlsx)")
        
        # Verify content has data
        import pandas as pd
        df = pd.read_excel(io.BytesIO(res.content))
        print(f"Exported rows: {len(df)}")
        if len(df) > 0:
            print("✅ Exported file contains data rows")
            print("Columns:", list(df.columns))
            print("First row:", df.iloc[0].to_dict())
            print("\n✅ Excel Export test PASSED!")
        else:
            print("❌ Exported file is EMPTY!")
    else:
        print("❌ Export test FAILED!")

if __name__ == '__main__':
    main()
