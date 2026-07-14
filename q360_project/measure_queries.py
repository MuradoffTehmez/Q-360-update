"""Server-side audit: hits every page with Django test client, records
status, DB query count and render duration. Run inside the web container:
docker compose exec web python measure_queries.py [--json out.json]
"""
import json
import os
import sys
import time

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import connection, reset_queries
from django.test.utils import CaptureQueriesContext
from django.test import Client

PAGES_JSON = os.path.join(os.path.dirname(__file__), 'pages_audit.json')
pages = json.load(open(PAGES_JSON, encoding='utf-8'))

client = Client()
User = get_user_model()
user = User.objects.get(username='test_admin')
client.force_login(user)

anon = Client()

results = []
for section, use_auth in (('public', False), ('auth', True)):
    c = client if use_auth else anon
    for entry in pages[section]:
        url = entry['url']
        try:
            reset_queries()
            with CaptureQueriesContext(connection) as ctx:
                t0 = time.perf_counter()
                resp = c.get(url, follow=False)
                dt = (time.perf_counter() - t0) * 1000
            dup = 0
            seen = {}
            for q in ctx.captured_queries:
                sql = q['sql']
                seen[sql] = seen.get(sql, 0) + 1
            dup = sum(v - 1 for v in seen.values() if v > 1)
            results.append({
                'name': entry['name'], 'url': url, 'status': resp.status_code,
                'ms': round(dt, 1), 'queries': len(ctx.captured_queries),
                'dup_queries': dup,
                'redirect': resp.get('Location', '') if resp.status_code in (301, 302) else '',
            })
            r = results[-1]
            print(f"{r['status']} {r['ms']:8.1f}ms q={r['queries']:3d} dup={r['dup_queries']:3d} {r['name']:30s} {r['redirect']}")
        except Exception as e:
            results.append({'name': entry['name'], 'url': url, 'error': str(e)[:200]})
            print('ERR', entry['name'], str(e)[:150])

out = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else 'query_audit.json'
json.dump(results, open(out, 'w', encoding='utf-8'), indent=1)
print('saved', out)
