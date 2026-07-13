from rest_framework.test import APITestCase
from rest_framework import status
from apps.accounts.models import User
from apps.performance_reviews.models import ReviewSession, ReviewNote, ReviewActionItem, CompetencyEvaluation
from apps.competencies.models import Competency

class PerformanceReviewCRUDTests(APITestCase):
    def setUp(self):
        self.manager = User.objects.create(username='manager', role='manager')
        self.employee = User.objects.create(username='employee', role='employee')
        self.other_user = User.objects.create(username='other', role='employee')
        from django.utils import timezone
        self.session = ReviewSession.objects.create(
            manager=self.manager,
            employee=self.employee,
            status='scheduled',
            date=timezone.now()
        )
        self.competency = Competency.objects.create(
            name="Leadership",
            description="Leads teams effectively"
        )
        
        self.note = ReviewNote.objects.create(session=self.session, topic='General', content='Old note')
        self.action_item = ReviewActionItem.objects.create(session=self.session, description='Old AI')

    # 1. Notes Tests
    def test_create_note_manager(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post('/api/v1/performance-reviews/notes/', {
            'session': self.session.id,
            'topic': 'General',
            'content': 'New note'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ReviewNote.objects.filter(content='New note').exists())

    def test_create_note_employee(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.post('/api/v1/performance-reviews/notes/', {
            'session': self.session.id,
            'topic': 'General',
            'content': 'Hacked note'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_note_manager(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.patch(f'/api/v1/performance-reviews/notes/{self.note.id}/', {
            'content': 'Updated note'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.content, 'Updated note')

    # 2. Action Items Tests
    def test_create_action_item_manager(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post('/api/v1/performance-reviews/action-items/', {
            'session': self.session.id,
            'description': 'New AI'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_action_item_employee(self):
        self.client.force_authenticate(user=self.employee)
        response = self.client.post('/api/v1/performance-reviews/action-items/', {
            'session': self.session.id,
            'description': 'Hacked AI'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # 3. Competency Evaluations Tests
    def test_create_competency_eval_manager(self):
        from apps.competencies.models import ProficiencyLevel
        prof_level = ProficiencyLevel.objects.create(name='advanced', display_name='Advanced', score_min=3.0, score_max=4.0)
        self.client.force_authenticate(user=self.manager)
        response = self.client.post('/api/v1/performance-reviews/competency-evaluations/', {
            'session': self.session.id,
            'competency': self.competency.id,
            'manager_rating': prof_level.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_competency_eval_employee(self):
        from apps.competencies.models import ProficiencyLevel
        prof_level = ProficiencyLevel.objects.create(name='expert', display_name='Expert', score_min=4.0, score_max=5.0)
        self.client.force_authenticate(user=self.employee)
        response = self.client.post('/api/v1/performance-reviews/competency-evaluations/', {
            'session': self.session.id,
            'competency': self.competency.id,
            'manager_rating': prof_level.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # 4. Old Action Consistency Tests
    def test_old_action_add_note_works(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.post(f'/api/v1/performance-reviews/sessions/{self.session.id}/add_note/', {
            'topic': 'General',
            'content': 'Note from old action'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ReviewNote.objects.filter(content='Note from old action').exists())
