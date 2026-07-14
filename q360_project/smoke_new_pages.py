import os
import django
from django.test.client import Client
from django.urls import get_resolver
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()
try:
    user = User.objects.get(username='admin')
except User.DoesNotExist:
    user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')

client = Client()
client.force_login(user)

resolver = get_resolver()
urls_to_test = []

def extract_urls(urlpatterns, prefix=''):
    for pattern in urlpatterns:
        if hasattr(pattern, 'url_patterns'):
            extract_urls(pattern.url_patterns, prefix + str(pattern.pattern))
        else:
            url = prefix + str(pattern.pattern)
            url = url.replace('^', '/').replace('$', '').replace('<int:pk>', '1').replace('<int:id>', '1').replace('<str:username>', 'admin')
            if not url.startswith('/'):
                url = '/' + url
            if 'admin' not in url and 'api' not in url:
                urls_to_test.append(url)

extract_urls(resolver.url_patterns)

results = {'pass': 0, 'fail': [], 'total': 0}
for url in set(urls_to_test):
    try:
        response = client.get(url)
        if response.status_code in [200, 301, 302]:
            results['pass'] += 1
        else:
            results['fail'].append((url, response.status_code))
    except Exception as e:
        results['fail'].append((url, str(e)))
    results['total'] += 1

print(f"Total tested: {results['total']}")
print(f"Passed: {results['pass']}")
if results['fail']:
    print("Failed URLs:")
    for url, err in results['fail']:
        print(f"{url} -> {err}")
