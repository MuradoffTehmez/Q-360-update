import os, sys, re

apps_dir = 'apps'
apps = [d for d in os.listdir(apps_dir) if os.path.isdir(os.path.join(apps_dir, d)) and not d.startswith('__')]
print(f'Total apps found: {len(apps)}')

try:
    with open('config/api_urls.py', 'r', encoding='utf-8') as f:
        api_urls = f.read()
except FileNotFoundError:
    api_urls = ""

results = []
for app in apps:
    app_path = os.path.join(apps_dir, app)
    has_serializers = os.path.exists(os.path.join(app_path, 'serializers.py'))
    
    viewset_count = 0
    serializer_count = 0
    
    for filename in ['views.py', 'api_views.py', 'api.py']:
        filepath = os.path.join(app_path, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                viewset_count += len(re.findall(r'class \w+ViewSet', content))
                
    if has_serializers:
        with open(os.path.join(app_path, 'serializers.py'), 'r', encoding='utf-8') as f:
            content = f.read()
            serializer_count = len(re.findall(r'class \w+Serializer', content))
            
    is_registered = app in api_urls
    
    # check for tests
    test_count = 0
    tests_dir = os.path.join(app_path, 'tests')
    tests_py = os.path.join(app_path, 'tests.py')
    
    if os.path.exists(tests_dir):
        for root, dirs, files in os.walk(tests_dir):
            for f in files:
                if f.endswith('.py'):
                    with open(os.path.join(root, f), 'r', encoding='utf-8') as tf:
                        content = tf.read()
                        test_count += len(re.findall(r'def test_', content))
    elif os.path.exists(tests_py):
        with open(tests_py, 'r', encoding='utf-8') as tf:
            content = tf.read()
            test_count += len(re.findall(r'def test_', content))
            
    # check for permissions
    permissions = []
    for filename in ['views.py', 'api_views.py', 'api.py']:
        filepath = os.path.join(app_path, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                perms = re.findall(r'permission_classes\s*=\s*\[(.*?)\]', content)
                for p in perms:
                    items = [x.strip() for x in p.split(',')]
                    for item in items:
                        if item and item not in permissions:
                            permissions.append(item)
    
    results.append({
        'app': app,
        'serializers': serializer_count,
        'viewsets': viewset_count,
        'registered': is_registered,
        'test_count': test_count,
        'permissions': ', '.join(permissions) if permissions else 'None'
    })

print(f'| Module | API exists (y/n) | Serializers | ViewSets | Router registration | Permission classes | Test count |')
print(f'|---|---|---|---|---|---|---|')
for r in sorted(results, key=lambda x: x['app']):
    has_api = 'y' if r['viewsets'] > 0 else 'n'
    reg = 'y' if r['registered'] else 'n'
    print(f'| {r["app"]} | {has_api} | {r["serializers"]} | {r["viewsets"]} | {reg} | {r["permissions"]} | {r["test_count"]} |')
