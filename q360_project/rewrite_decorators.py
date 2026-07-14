import os
import glob
import re

APPS = ['workflow_engine', 'approval_engine', 'access_control', 'policy_engine', 'feature_flags']
BASE_DIR = '/app/apps'

for app in APPS:
    for filename in ['template_views.py', 'views_extras.py']:
        path = os.path.join(BASE_DIR, app, filename)
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace the user_passes_test import
        content = re.sub(r'from django\.contrib\.auth\.decorators import user_passes_test\n?', '', content)
        
        # Add core.decorators import
        if 'superuser_required' not in content:
            # find first import
            content = "from apps.core.decorators import superuser_required\n" + content
            
        # Replace @user_passes_test(...)
        content = re.sub(r'@user_passes_test\(lambda u: u\.is_superuser\)', '@superuser_required', content)
        content = re.sub(r'@user_passes_test\(lambda u: u\.is_superuser or u\.has_perm\([^)]+\)\)', '@superuser_required', content)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {path}")
