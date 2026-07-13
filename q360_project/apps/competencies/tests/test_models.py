"""
Tests for competencies models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.competencies.models import (
    Competency, ProficiencyLevel, PositionCompetency, UserSkill
)
from apps.departments.models import Organization, Department, Position

User = get_user_model()

class CompetencyModelTest(TestCase):
    """Test Competency model."""

    def test_create_competency(self):
        """Test creating a competency."""
        competency = Competency.objects.create(
            name='Python Programming',
            description='Advanced Python coding skills',
            is_active=True
        )

        self.assertEqual(competency.name, 'Python Programming')
        self.assertTrue(competency.is_active)
        self.assertEqual(str(competency), 'Python Programming')


class ProficiencyLevelModelTest(TestCase):
    """Test ProficiencyLevel model."""

    def test_create_proficiency_level(self):
        """Test creating a proficiency level."""
        level = ProficiencyLevel.objects.create(
            name='intermediate',
            display_name='Orta',
            score_min=40.0,
            score_max=69.99
        )

        self.assertEqual(level.name, 'intermediate')
        self.assertEqual(str(level), 'Orta (40.0-69.99)')


class PositionCompetencyModelTest(TestCase):
    """Test PositionCompetency model."""

    def setUp(self):
        self.org = Organization.objects.create(name="Test Org")
        self.dept = Department.objects.create(name="Test Dept", organization=self.org)
        self.position = Position.objects.create(
            title="Software Engineer",
            department=self.dept,
            is_active=True
        )
        self.competency = Competency.objects.create(
            name='Django',
            is_active=True
        )
        self.level = ProficiencyLevel.objects.create(
            name='advanced',
            display_name='Təkmil',
            score_min=70.0,
            score_max=89.99
        )

    def test_create_position_competency(self):
        """Test assigning competency to a position."""
        pos_comp = PositionCompetency.objects.create(
            position=self.position,
            competency=self.competency,
            required_level=self.level,
            weight=0.8,
            is_mandatory=True
        )

        self.assertEqual(pos_comp.position, self.position)
        self.assertEqual(pos_comp.competency, self.competency)
        self.assertTrue(pos_comp.is_mandatory)


class UserSkillModelTest(TestCase):
    """Test UserSkill model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='skilluser',
            email='skill@test.com',
            password='testpass123'
        )
        self.competency = Competency.objects.create(
            name='Communication',
            is_active=True
        )
        self.level = ProficiencyLevel.objects.create(
            name='expert',
            display_name='Ekspert',
            score_min=90.0,
            score_max=100.0
        )

    def test_create_user_skill(self):
        """Test assigning skill to user."""
        user_skill = UserSkill.objects.create(
            user=self.user,
            competency=self.competency,
            level=self.level,
            years_of_experience=5,
            is_approved=True
        )

        self.assertEqual(user_skill.user, self.user)
        self.assertEqual(user_skill.competency, self.competency)
        self.assertTrue(user_skill.is_approved)
