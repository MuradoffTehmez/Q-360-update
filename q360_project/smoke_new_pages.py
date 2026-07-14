"""Smoke test for newly built pages.
Usage: docker compose exec -T web python smoke_new_pages.py <urls_file> [--user test_admin]
urls_file: one URL per line (# comment lines ignored).
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client

urls_file = sys.argv[1]
username = sys.argv[sys.argv.index('--user') + 1] if '--user' in sys.argv else 'test_admin'

User = get_user_model()
client = Client()
user = User.objects.get(username=username)
client.force_login(user)

urls = [l.strip() for l in open(urls_file, encoding='utf-8')
        if l.strip() and not l.startswith('#')]

fails = 0
for url in urls:
    try:
        resp = client.get(url)
        status = resp.status_code
        mark = 'OK ' if status == 200 else ('RED' if status in (301, 302) else 'FAIL')
        if status != 200:
            fails += 1
        loc = resp.get('Location', '') if status in (301, 302) else ''
        print(f'{mark} {status} {url} {loc}')
    except Exception as e:
        fails += 1
        print(f'EXC     {url} {type(e).__name__}: {str(e)[:160]}')

print(f'\n{len(urls) - fails}/{len(urls)} OK (user={username})')
sys.exit(1 if fails else 0)
