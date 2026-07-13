with open('locale/az/LC_MESSAGES/django.po', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Remove fuzzy and update translation
content = content.replace('#, fuzzy\n#| msgid "Son Giriş"\nmsgid "Giriş"\nmsgstr "Last Login"', 'msgid "Giriş"\nmsgstr "Xoş Gəldiniz (Tərcümə Testi)"')

with open('locale/az/LC_MESSAGES/django.po', 'w', encoding='utf-8') as f:
    f.write(content)

import subprocess
import requests
import re

print("Compiling messages...")
subprocess.run(["python", "manage.py", "compilemessages"], check=True)
print("Compilation done.")

print("\nFetching login page...")
import time
time.sleep(5)
html = requests.get('http://localhost:8000/accounts/login/', headers={'Accept-Language': 'az'}).text

# Extract title
title_match = re.search(r'<title>(.*?)</title>', html)
if title_match:
    print(f"TITLE: {title_match.group(1)}")
else:
    print("Title not found")
