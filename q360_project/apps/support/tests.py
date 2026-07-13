"""
Tests for the Support / Help Desk module.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.support.models import SupportTicket, TicketComment

User = get_user_model()


class SupportTicketModelTest(TestCase):
    """Tests for the SupportTicket model."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='support_user',
            email='support_user@test.com',
            password='TestPass123!',
            first_name='Leyla',
            last_name='Hüseynova',
        )
        cls.support_agent = User.objects.create_user(
            username='support_agent',
            email='agent@test.com',
            password='TestPass123!',
            first_name='Support',
            last_name='Agent',
        )

    def test_create_ticket(self):
        """Test creating a basic support ticket."""
        ticket = SupportTicket.objects.create(
            title='Sistemə daxil ola bilmirəm',
            description='Login səhifəsində xəta alıram.',
            created_by=self.user,
            priority='high',
        )
        self.assertEqual(ticket.title, 'Sistemə daxil ola bilmirəm')
        self.assertEqual(ticket.status, 'open')
        self.assertEqual(ticket.priority, 'high')
        self.assertEqual(ticket.created_by, self.user)
        self.assertIsNone(ticket.assigned_to)
        self.assertIsNone(ticket.resolved_at)

    def test_ticket_assignment(self):
        """Test assigning a ticket to a support agent."""
        ticket = SupportTicket.objects.create(
            title='Hesabat yüklənmir',
            description='PDF hesabat boş gəlir.',
            created_by=self.user,
        )
        ticket.assigned_to = self.support_agent
        ticket.status = 'in_progress'
        ticket.save()

        ticket.refresh_from_db()
        self.assertEqual(ticket.assigned_to, self.support_agent)
        self.assertEqual(ticket.status, 'in_progress')

    def test_ticket_resolution(self):
        """Test resolving a support ticket."""
        from django.utils import timezone

        ticket = SupportTicket.objects.create(
            title='Şifrə sıfırlama işləmir',
            description='E-poçt gəlmir.',
            created_by=self.user,
            assigned_to=self.support_agent,
        )
        ticket.status = 'resolved'
        ticket.resolved_at = timezone.now()
        ticket.save()

        ticket.refresh_from_db()
        self.assertEqual(ticket.status, 'resolved')
        self.assertIsNotNone(ticket.resolved_at)

    def test_ticket_str_representation(self):
        """Test string representation of a ticket."""
        ticket = SupportTicket.objects.create(
            title='Test sorğusu',
            description='Test',
            created_by=self.user,
        )
        str_repr = str(ticket)
        self.assertIn('Test sorğusu', str_repr)
        self.assertIn('Açıq', str_repr)

    def test_ticket_ordering(self):
        """Test tickets are ordered by creation date descending."""
        t1 = SupportTicket.objects.create(
            title='Birinci',
            description='Test 1',
            created_by=self.user,
        )
        t2 = SupportTicket.objects.create(
            title='İkinci',
            description='Test 2',
            created_by=self.user,
        )
        tickets = list(SupportTicket.objects.all())
        self.assertEqual(tickets[0], t2)
        self.assertEqual(tickets[1], t1)

    def test_default_priority_is_medium(self):
        """Test that default priority is 'medium'."""
        ticket = SupportTicket.objects.create(
            title='Default prioritet',
            description='Test',
            created_by=self.user,
        )
        self.assertEqual(ticket.priority, 'medium')


class TicketCommentModelTest(TestCase):
    """Tests for the TicketComment model."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='comment_user',
            email='comment@test.com',
            password='TestPass123!',
        )
        cls.ticket = SupportTicket.objects.create(
            title='Comment test sorğusu',
            description='Test',
            created_by=cls.user,
        )

    def test_create_comment(self):
        """Test adding a comment to a ticket."""
        comment = TicketComment.objects.create(
            ticket=self.ticket,
            comment='Problem araşdırılır.',
            created_by=self.user,
        )
        self.assertEqual(comment.ticket, self.ticket)
        self.assertEqual(comment.comment, 'Problem araşdırılır.')
        self.assertFalse(comment.is_internal)

    def test_internal_comment(self):
        """Test creating an internal-only comment."""
        comment = TicketComment.objects.create(
            ticket=self.ticket,
            comment='Daxili qeyd: DB-də yoxla.',
            created_by=self.user,
            is_internal=True,
        )
        self.assertTrue(comment.is_internal)

    def test_comment_ordering(self):
        """Test comments are ordered by creation date ascending."""
        c1 = TicketComment.objects.create(
            ticket=self.ticket,
            comment='Birinci cavab',
            created_by=self.user,
        )
        c2 = TicketComment.objects.create(
            ticket=self.ticket,
            comment='İkinci cavab',
            created_by=self.user,
        )
        comments = list(self.ticket.comments.all())
        self.assertEqual(comments[0], c1)
        self.assertEqual(comments[1], c2)

    def test_ticket_comment_relationship(self):
        """Test that comments are properly linked to tickets."""
        TicketComment.objects.create(
            ticket=self.ticket,
            comment='Test 1',
            created_by=self.user,
        )
        TicketComment.objects.create(
            ticket=self.ticket,
            comment='Test 2',
            created_by=self.user,
        )
        self.assertEqual(self.ticket.comments.count(), 2)
