"""
Tests for the Workforce Planning module.
"""
from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.departments.models import Organization, Department, Position
from apps.workforce_planning.models import TalentMatrix, CriticalRole

User = get_user_model()


class TalentMatrixModelTest(TestCase):
    """Tests for the TalentMatrix (9-Box) model."""

    @classmethod
    def setUpTestData(cls):
        cls.employee = User.objects.create_user(
            username='wfp_employee',
            email='wfp_emp@test.com',
            password='TestPass123!',
            first_name='Ali',
            last_name='Mammadov',
        )
        cls.manager = User.objects.create_user(
            username='wfp_manager',
            email='wfp_mgr@test.com',
            password='TestPass123!',
            first_name='Kamran',
            last_name='Əliyev',
        )

    def test_create_talent_assessment(self):
        """Test creating a 9-Box talent assessment."""
        assessment = TalentMatrix.objects.create(
            user=self.employee,
            performance_level='high',
            potential_level='high',
            performance_score=Decimal('85.00'),
            potential_score=Decimal('90.00'),
            assessed_by=self.manager,
            assessment_date=date.today(),
            assessment_period='2026 Q2',
        )
        self.assertEqual(assessment.user, self.employee)
        self.assertEqual(assessment.performance_level, 'high')
        self.assertEqual(assessment.potential_level, 'high')

    def test_auto_box_calculation(self):
        """Test that box_category is automatically calculated on save."""
        # High performance + High potential = box9
        assessment = TalentMatrix.objects.create(
            user=self.employee,
            performance_level='high',
            potential_level='high',
            performance_score=Decimal('90.00'),
            potential_score=Decimal('92.00'),
            assessed_by=self.manager,
            assessment_date=date.today(),
            assessment_period='2026 Q2',
        )
        self.assertEqual(assessment.box_category, 'box9')

    def test_box_calculation_low_low(self):
        """Test box1: Low performance + Low potential."""
        assessment = TalentMatrix.objects.create(
            user=self.employee,
            performance_level='low',
            potential_level='low',
            performance_score=Decimal('20.00'),
            potential_score=Decimal('15.00'),
            assessed_by=self.manager,
            assessment_date=date.today(),
            assessment_period='2026 Q2',
        )
        self.assertEqual(assessment.box_category, 'box1')

    def test_box_calculation_medium_high(self):
        """Test box6: Medium performance + High potential."""
        assessment = TalentMatrix.objects.create(
            user=self.employee,
            performance_level='medium',
            potential_level='high',
            performance_score=Decimal('60.00'),
            potential_score=Decimal('85.00'),
            assessed_by=self.manager,
            assessment_date=date.today(),
            assessment_period='2026 Q2',
        )
        self.assertEqual(assessment.box_category, 'box6')

    def test_str_representation(self):
        """Test string representation of a talent assessment."""
        assessment = TalentMatrix.objects.create(
            user=self.employee,
            performance_level='high',
            potential_level='medium',
            performance_score=Decimal('80.00'),
            potential_score=Decimal('65.00'),
            assessed_by=self.manager,
            assessment_date=date.today(),
            assessment_period='2026 Q1',
        )
        str_repr = str(assessment)
        self.assertIn(self.employee.get_full_name(), str_repr)
        self.assertIn('2026 Q1', str_repr)

    def test_ordering(self):
        """Test assessments are ordered by date descending."""
        old = TalentMatrix.objects.create(
            user=self.employee,
            performance_level='medium',
            potential_level='medium',
            performance_score=Decimal('50.00'),
            potential_score=Decimal('50.00'),
            assessed_by=self.manager,
            assessment_date=date(2025, 1, 1),
            assessment_period='2025 Q1',
        )
        new = TalentMatrix.objects.create(
            user=self.employee,
            performance_level='high',
            potential_level='high',
            performance_score=Decimal('90.00'),
            potential_score=Decimal('90.00'),
            assessed_by=self.manager,
            assessment_date=date(2026, 6, 1),
            assessment_period='2026 Q2',
        )
        assessments = list(TalentMatrix.objects.all())
        self.assertEqual(assessments[0], new)


class CriticalRoleModelTest(TestCase):
    """Tests for the CriticalRole model."""

    @classmethod
    def setUpTestData(cls):
        cls.org = Organization.objects.create(
            name='Test Təşkilat',
            code='TST01',
        )
        cls.dept = Department.objects.create(
            name='IT Şöbəsi',
            code='IT01',
            organization=cls.org,
        )
        cls.position = Position.objects.create(
            title='Baş Mühəndis',
            code='BM01',
            department=cls.dept,
            organization=cls.org,
        )

    def test_create_critical_role(self):
        """Test creating a critical role entry."""
        role = CriticalRole.objects.create(
            position=self.position,
            criticality_level='high',
            business_impact='Təşkilat üçün kritik rol',
            succession_readiness='needs_development',
        )
        self.assertEqual(role.position, self.position)
        self.assertEqual(role.criticality_level, 'high')
