"""
Tests for the Wellness & Well-Being module.
"""
from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from apps.wellness.models import (
    HealthCheckup,
    MentalHealthSurvey,
)

User = get_user_model()


class HealthCheckupModelTest(TestCase):
    """Tests for the HealthCheckup model."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test_wellness_user',
            email='wellness@test.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User',
        )

    def test_create_health_checkup(self):
        """Test creating a basic health checkup record."""
        checkup = HealthCheckup.objects.create(
            employee=self.user,
            checkup_type='general',
            scheduled_date=timezone.now() + timedelta(days=7),
            status='scheduled',
            provider='Dövlət Poliklinikası',
            location='Bakı, Azərbaycan',
        )
        self.assertEqual(checkup.employee, self.user)
        self.assertEqual(checkup.checkup_type, 'general')
        self.assertEqual(checkup.status, 'scheduled')
        self.assertFalse(checkup.reminder_sent)

    def test_checkup_status_transitions(self):
        """Test checkup status can be changed through its lifecycle."""
        checkup = HealthCheckup.objects.create(
            employee=self.user,
            checkup_type='annual',
            scheduled_date=timezone.now() + timedelta(days=1),
        )
        self.assertEqual(checkup.status, 'scheduled')

        checkup.status = 'completed'
        checkup.completed_date = timezone.now()
        checkup.results = 'Bütün nəticələr normaldır.'
        checkup.save()

        checkup.refresh_from_db()
        self.assertEqual(checkup.status, 'completed')
        self.assertIsNotNone(checkup.completed_date)

    def test_checkup_str_representation(self):
        """Test string representation of a health checkup."""
        checkup = HealthCheckup.objects.create(
            employee=self.user,
            checkup_type='blood_test',
            scheduled_date=timezone.now(),
        )
        str_repr = str(checkup)
        self.assertIn(self.user.get_full_name(), str_repr)

    def test_checkup_ordering(self):
        """Test that checkups are ordered by scheduled_date descending."""
        old = HealthCheckup.objects.create(
            employee=self.user,
            checkup_type='general',
            scheduled_date=timezone.now() - timedelta(days=30),
        )
        new = HealthCheckup.objects.create(
            employee=self.user,
            checkup_type='dental',
            scheduled_date=timezone.now() + timedelta(days=7),
        )
        checkups = list(HealthCheckup.objects.all())
        self.assertEqual(checkups[0], new)
        self.assertEqual(checkups[1], old)

    def test_cancelled_checkup(self):
        """Test that a checkup can be cancelled."""
        checkup = HealthCheckup.objects.create(
            employee=self.user,
            checkup_type='vision',
            scheduled_date=timezone.now() + timedelta(days=14),
        )
        checkup.status = 'cancelled'
        checkup.save()
        checkup.refresh_from_db()
        self.assertEqual(checkup.status, 'cancelled')


class MentalHealthSurveyModelTest(TestCase):
    """Tests for the MentalHealthSurvey model."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='test_mental_user',
            email='mental@test.com',
            password='TestPass123!',
        )

    def test_create_mental_health_survey(self):
        """Test creating a mental health survey response."""
        survey = MentalHealthSurvey.objects.create(
            employee=self.user,
            stress_level=3,
            workload_satisfaction=4,
            work_life_balance=4,
            sleep_quality=4,
            anxiety_level=2,
            comments='Normal iş şəraiti',
        )
        self.assertEqual(survey.employee, self.user)
        self.assertEqual(survey.stress_level, 3)
        self.assertIsNotNone(survey.survey_date)
