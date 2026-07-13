import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from apps.accounts.models import User
import re

client = Client()
user = User.objects.filter(is_active=True).first()
if user:
    client.force_login(user)
    # The accounts dashboard URL is likely /accounts/dashboard/ or /accounts/profile/
    response = client.get('/accounts/dashboard/')
    if response.status_code == 404:
        response = client.get('/accounts/profile/')
    
    html = response.content.decode('utf-8')
    
    # We are looking for text nodes that contain ">".
    # A simple regex to find ">" outside of tags
    # We'll just look for ">" that is immediately followed by some text, or spaces and text.
    # Actually, we can just split by lines and see which line has ">" but no "<" before it, or just find it.
    
    lines = html.split('\n')
    for i, line in enumerate(lines):
        # strip tags
        text = re.sub(r'<[^>]+>', '', line)
        if '>' in text:
            print(f"Possible stray at line {i+1}: {line.strip()}")
            print(f"Text content: {text.strip()}")
