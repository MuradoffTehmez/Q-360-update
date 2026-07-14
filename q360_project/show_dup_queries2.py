"""Print duplicated SQL queries (tail end with WHERE) for a URL."""
import os
import sys
from collections import Counter

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.test import Client

url = sys.argv[1]
client = Client()
User = get_user_model()
client.force_login(User.objects.get(username='test_admin'))

with CaptureQueriesContext(connection) as ctx:
    resp = client.get(url)
print('status', resp.status_code, 'queries', len(ctx.captured_queries))
counts = Counter(q['sql'] for q in ctx.captured_queries)
for sql, n in counts.most_common(10):
    if n > 1:
        table = sql.split('FROM ')[1].split(' ')[0] if 'FROM ' in sql else '?'
        where = sql.split('WHERE')[1][:150] if 'WHERE' in sql else '(no where)'
        print(f' x{n}: {table} WHERE {where}')
