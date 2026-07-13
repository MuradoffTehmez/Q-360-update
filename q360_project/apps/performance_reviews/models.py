"""
Models for performance_reviews app - Manager-Employee 1-on-1s.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.competencies.models import Competency, ProficiencyLevel


class ReviewSession(models.Model):
    """
    Represents a 1-on-1 performance review session between a manager and an employee.
    """
    STATUS_CHOICES = [
        ('scheduled', 'Planlaşdırılıb'),
        ('in_progress', 'Davam Edir'),
        ('completed', 'Tamamlanıb'),
        ('cancelled', 'Ləğv Edilib'),
    ]

    manager = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='conducted_reviews',
        verbose_name=_('Rəhbər')
    )
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_reviews',
        verbose_name=_('İşçi')
    )
    
    date = models.DateTimeField(verbose_name=_('Görüş Tarixi'))
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='scheduled',
        verbose_name=_('Status')
    )
    overall_notes = models.TextField(
        blank=True, verbose_name=_('Ümumi Qeydlər')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('1-on-1 Görüş')
        verbose_name_plural = _('1-on-1 Görüşlər')
        ordering = ['-date']

    def __str__(self):
        return f"{self.manager} -> {self.employee} ({self.date.strftime('%Y-%m-%d')})"


class ReviewNote(models.Model):
    """
    Specific discussion points or topics during the review session.
    """
    session = models.ForeignKey(
        ReviewSession, on_delete=models.CASCADE, related_name='notes'
    )
    topic = models.CharField(max_length=200, verbose_name=_('Mövzu'))
    content = models.TextField(verbose_name=_('Məzmun'))
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Görüş Qeydi')
        verbose_name_plural = _('Görüş Qeydləri')


class ReviewActionItem(models.Model):
    """
    Action items decided during the 1-on-1 session.
    """
    session = models.ForeignKey(
        ReviewSession, on_delete=models.CASCADE, related_name='action_items'
    )
    description = models.CharField(max_length=500, verbose_name=_('Təsvir'))
    due_date = models.DateField(null=True, blank=True, verbose_name=_('Bitmə Tarixi'))
    is_completed = models.BooleanField(default=False, verbose_name=_('Tamamlanıb'))
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Görüləcək İş')
        verbose_name_plural = _('Görüləcək İşlər')


class CompetencyEvaluation(models.Model):
    """
    Manager's evaluation of the employee's competencies during the 1-on-1.
    """
    session = models.ForeignKey(
        ReviewSession, on_delete=models.CASCADE, related_name='competency_evaluations'
    )
    competency = models.ForeignKey(
        Competency, on_delete=models.CASCADE, related_name='manager_evaluations'
    )
    manager_rating = models.ForeignKey(
        ProficiencyLevel, on_delete=models.RESTRICT, null=True, blank=True,
        verbose_name=_('Rəhbər Qiymətləndirməsi')
    )
    comment = models.TextField(blank=True, verbose_name=_('Rəy/Şərh'))

    class Meta:
        verbose_name = _('Kompetensiya Qiymətləndirməsi')
        verbose_name_plural = _('Kompetensiya Qiymətləndirmələri')
        unique_together = ('session', 'competency')

    def __str__(self):
        return f"{self.competency} - {self.manager_rating}"
