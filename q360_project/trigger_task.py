import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.tasks import import_users_task

def main():
    print("Triggering import_users_task to Celery...")
    res = import_users_task.delay('dummy.csv', 16)
    print(f"Task ID: {res.id}")
    try:
        print(f"Task Result: {res.get(timeout=5)}")
    except Exception as e:
        print(f"Error getting result: {e}")

if __name__ == '__main__':
    main()
