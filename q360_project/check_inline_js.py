"""Fetch a rendered page (authenticated) and syntax-check each inline script.
Usage: python check_inline_js.py /dashboard/ai-management/ [more urls...]
Runs on host; talks to http://localhost:8000 with a real session login.
"""
import re
import subprocess
import sys
import tempfile
import os
import requests

BASE = 'http://localhost:8000'

s = requests.Session()
r = s.get(BASE + '/accounts/login/')
csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text).group(1)
r = s.post(BASE + '/accounts/login/',
           data={'csrfmiddlewaretoken': csrf, 'username': 'test_admin', 'password': 'testpass123'},
           headers={'Referer': BASE + '/accounts/login/'})
assert '/login' not in r.url, 'login failed'

for url in sys.argv[1:]:
    html = s.get(BASE + url).text
    scripts = re.findall(r'<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>', html, re.S)
    print(f'== {url}: {len(scripts)} inline scripts')
    for i, (attrs, body) in enumerate(scripts):
        if 'ld+json' in attrs or 'application/json' in attrs or not body.strip():
            continue
        fd, path = tempfile.mkstemp(suffix='.js')
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(body)
        res = subprocess.run(['node', '--check', path], capture_output=True, text=True)
        if res.returncode != 0:
            first = res.stderr.splitlines()
            # extract line number from "path:NN"
            ln = None
            for line in first:
                m = re.match(r'.*\.js:(\d+)', line)
                if m:
                    ln = int(m.group(1))
                    break
            print(f'  BAD script #{i} attrs={attrs.strip()[:50]}')
            if ln:
                lines = body.split('\n')
                lo = max(0, ln - 4)
                for j in range(lo, min(len(lines), ln + 2)):
                    mark = '>>' if j + 1 == ln else '  '
                    print(f'   {mark} {j+1:4d} {lines[j][:160]}')
            print('   ', first[-1][:200] if first else '')
        os.unlink(path)
