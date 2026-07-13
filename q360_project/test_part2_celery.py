import os
import django
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.evaluations.models import EvaluationCampaign
from apps.accounts.models import User
from apps.notifications.models import Notification
from apps.evaluations.tasks import send_deadline_reminders
from apps.departments.models import Department, Organization

def main():
    print("=== A.2 DEADLINE REMINDER TEST ===")
    
    # 1. Create a campaign with past deadline
    org = Organization.objects.first()
    dept, _ = Department.objects.get_or_create(name='TestDept', code='TEST', organization=org)
    user, _ = User.objects.get_or_create(username='eval_user', email='eval@test.com')
    
    past_date = timezone.now() - timedelta(days=2)
    campaign, created = EvaluationCampaign.objects.get_or_create(
        title="Test Campaign Past Deadline",
        defaults={
            'start_date': past_date - timedelta(days=10),
            'end_date': past_date,
            'status': 'active',
            'created_by': user
        }
    )
    
    if not created:
        campaign.end_date = past_date
        campaign.status = 'active'
        campaign.save()
        
    print(f"1. Campaign ID {campaign.id} created/updated with deadline {campaign.end_date}")
    
    # Create Assignment
    from apps.evaluations.models import EvaluationAssignment
    assignment, _ = EvaluationAssignment.objects.get_or_create(
        campaign=campaign,
        evaluator=user,
        evaluatee=user,
        defaults={'status': 'pending'}
    )
    if assignment.status != 'pending':
        assignment.status = 'pending'
        assignment.save()
    
    from apps.notifications.models import NotificationTemplate
    NotificationTemplate.objects.get_or_create(
        trigger='deadline_reminder',
        defaults={
            'name': 'Deadline Reminder',
            'subject': 'Deadline Reminder Subject',
            'inapp_content': 'Your deadline is approaching',
            'is_active': True
        }
    )
    
    # Track existing notifications
    prev_notifs = Notification.objects.count()
    
    # 2. Trigger task manually
    print("\n2. Triggering send_deadline_reminders task...")
    res = send_deadline_reminders.delay()
    print(f"Task queued. ID: {res.id}")
    
    # Wait for celery to process
    try:
        res.get(timeout=10)
        print("Task finished successfully!")
    except Exception as e:
        print(f"Task raised exception: {e}")
        
    # 3. Check notifications
    new_notifs = Notification.objects.count()
    print(f"\n3. Notifications count before: {prev_notifs}, after: {new_notifs}")
    created_notifs = new_notifs - prev_notifs
    print(f"Newly created notifications: {created_notifs}")
    
    # 4. If any notification created, verify it's related to deadline
    recent = Notification.objects.filter(notification_type='reminder')
    print(f"Reminder notifications: {recent.count()}")
    for latest in recent:
        print(f"Notification: {latest.title} | {latest.message}")

if __name__ == '__main__':
    main()
