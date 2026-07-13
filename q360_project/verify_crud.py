import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from apps.accounts.models import User, Role
from apps.continuous_feedback.models import PublicRecognition, QuickFeedback
from apps.engagement.models import GamificationBadge, UserBadge
from apps.performance_reviews.models import ReviewSession, ReviewNote
import json

def run_tests():
    client = Client()

    # Create admin user
    admin, _ = User.objects.get_or_create(username='crud_admin', defaults={'is_superuser': True, 'is_staff': True, 'role': 'admin'})
    admin.set_password('admin123')
    admin.save()
    
    # Create regular user
    user1, _ = User.objects.get_or_create(username='crud_user1', defaults={'role': 'employee'})
    user1.set_password('user123')
    user1.save()

    Role._meta.get_field('name').choices.append(('test_role', 'Test Role'))
    Role._meta.get_field('name').choices.append(('test_role2', 'Test Role 2'))
    Role._meta.get_field('name').choices.append(('test_role_updated', 'Test Role Updated'))

    print("\n" + "="*50)
    print("1. ACCOUNTS/ROLES CRUD TEST")
    print("="*50)
    
    # POST as admin
    client.force_login(admin)
    res = client.post('/api/v1/accounts/roles/', {'name': 'test_role', 'display_name': 'Test Role', 'description': 'Test'}, content_type='application/json')
    print(f"[Admin POST] Status: {res.status_code}, Response: {res.json() if res.status_code != 500 else '500 ERROR'}")
    if res.status_code == 201:
        role_id = res.json().get('data', {}).get('id') or res.json().get('id')
        print(f"DB Check: Role exists? {Role.objects.filter(id=role_id).exists()}")
        
        # PUT as admin
        res = client.put(f'/api/v1/accounts/roles/{role_id}/', {'name': 'test_role_updated', 'display_name': 'Test Role Updated', 'description': 'Updated'}, content_type='application/json')
        print(f"[Admin PUT] Status: {res.status_code}")
        print(f"DB Check: Role name -> {Role.objects.get(id=role_id).name}")
        
        # DELETE as admin
        res = client.delete(f'/api/v1/accounts/roles/{role_id}/')
        print(f"[Admin DELETE] Status: {res.status_code}")
        print(f"DB Check: Role exists? {Role.objects.filter(id=role_id).exists()}")
    
    # Unauthorized POST
    client.force_login(user1)
    res = client.post('/api/v1/accounts/roles/', {'name': 'test_role2', 'display_name': 'Test Role 2'}, content_type='application/json')
    print(f"[User POST (Unauthorized)] Status: {res.status_code}")

    print("\n" + "="*50)
    print("2. CONTINUOUS FEEDBACK/PUBLIC RECOGNITION CRUD TEST")
    print("="*50)
    
    # Setup Feedback
    feedback = QuickFeedback.objects.create(sender=user1, recipient=admin, feedback_type='recognition', visibility='public', message='Test msg')
    
    # POST as sender (user1)
    client.force_login(user1)
    res = client.post('/api/v1/feedback/public-recognition/', {'feedback': feedback.id}, content_type='application/json')
    try:
        json_resp = res.json()
    except:
        json_resp = res.content
    print(f"[Sender POST] Status: {res.status_code}, Response: {json_resp}")
    if res.status_code == 201:
        rec_id = res.json().get('data', {}).get('id') or res.json().get('id')
        print(f"DB Check: PublicRecognition exists? {PublicRecognition.objects.filter(id=rec_id).exists()}")
        
        # PUT as sender
        res = client.patch(f'/api/v1/feedback/public-recognition/{rec_id}/', {'is_featured': True}, content_type='application/json')
        print(f"[Sender PATCH] Status: {res.status_code}")
        
        # Unauthorized DELETE
        client.force_login(admin)
        res = client.delete(f'/api/v1/feedback/public-recognition/{rec_id}/')
        print(f"[Other User DELETE] Status: {res.status_code}")
        
        # DELETE as sender
        client.force_login(user1)
        res = client.delete(f'/api/v1/feedback/public-recognition/{rec_id}/')
        print(f"[Sender DELETE] Status: {res.status_code}")
        print(f"DB Check: Exists? {PublicRecognition.objects.filter(id=rec_id).exists()}")

    print("\n" + "="*50)
    print("3. ENGAGEMENT/BADGES & USER-BADGES CRUD TEST")
    print("="*50)
    
    # Badges POST
    client.force_login(admin)
    res = client.post('/api/v1/engagement/badges/', {'name': 'Super Star', 'description': 'Test badge', 'category': 'performance', 'icon': 'star'}, content_type='application/json')
    print(f"[Admin POST Badge] Status: {res.status_code}")
    badge_id = res.json().get('data', {}).get('id') or res.json().get('id')
    
    # UserBadge POST
    res = client.post('/api/v1/engagement/user-badges/', {'user_id': user1.id, 'badge_id': badge_id}, content_type='application/json')
    print(f"[Admin POST UserBadge] Status: {res.status_code}")
    ub_id = res.json().get('data', {}).get('id') or res.json().get('id')
    
    # Unauthorized Badges POST
    client.force_login(user1)
    res = client.post('/api/v1/engagement/badges/', {'name': 'Fail Badge', 'description': 'Test badge', 'icon_class': 'star'}, content_type='application/json')
    print(f"[User POST Badge (Unauthorized)] Status: {res.status_code}")
    
    # DELETE
    client.force_login(admin)
    client.delete(f'/api/v1/engagement/user-badges/{ub_id}/')
    client.delete(f'/api/v1/engagement/badges/{badge_id}/')

    print("\n" + "="*50)
    print("4. PERFORMANCE REVIEWS/NOTES CRUD TEST")
    print("="*50)
    
    from django.utils import timezone
    session = ReviewSession.objects.create(manager=admin, employee=user1, status='scheduled', date=timezone.now())
    
    client.force_login(admin)
    res = client.post('/api/v1/performance-reviews/notes/', {'session': session.id, 'content': 'Test note'}, content_type='application/json')
    print(f"[Manager POST Note] Status: {res.status_code}")
    note_id = res.json().get('data', {}).get('id') or res.json().get('id')
    
    client.force_login(user1)
    res = client.put(f'/api/v1/performance-reviews/notes/{note_id}/', {'session': session.id, 'content': 'Hacked note'}, content_type='application/json')
    print(f"[Employee PUT Note (Unauthorized)] Status: {res.status_code}")
    
if __name__ == '__main__':
    run_tests()
