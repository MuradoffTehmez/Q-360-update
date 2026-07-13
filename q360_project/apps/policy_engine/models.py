from django.db import models
from apps.core.models import TimeStampedModel, SoftDeletableModel

class Policy(TimeStampedModel, SoftDeletableModel):
    CATEGORY_CHOICES = (
        ('HR', 'İnsan Resursları'),
        ('IT', 'İnformasiya Texnologiyaları'),
        ('FINANCE', 'Maliyyə'),
        ('SECURITY', 'Təhlükəsizlik'),
        ('COMPLIANCE', 'Uyğunluq'),
        ('GENERAL', 'Ümumi'),
    )
    name = models.CharField('Siyasət adı', max_length=255, unique=True)
    description = models.TextField('Açıqlama', blank=True)
    category = models.CharField('Kateqoriya', max_length=100, choices=CATEGORY_CHOICES, default='GENERAL')

    class Meta:
        verbose_name = 'Siyasət'
        verbose_name_plural = 'Siyasətlər'

    def __str__(self):
        return self.name

class PolicyVersion(TimeStampedModel):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='versions', verbose_name='Siyasət')
    version_number = models.PositiveIntegerField('Versiya nömrəsi')
    is_active = models.BooleanField('Aktiv versiya', default=False)
    rule_json = models.JSONField('Siyasət qaydaları (JSON)', help_text="Təşkilati siyasət qaydalarını JSONLogic formatında daxil edin. Məsələn: {\"if\": [{\">\": [{\"var\": \"leave_days\"}, 5]}, \"requires_approval\", \"auto_approve\"]}", default=dict, blank=True)

    class Meta:
        verbose_name = 'Siyasət Versiyası'
        verbose_name_plural = 'Siyasət Versiyaları'
        unique_together = ('policy', 'version_number')

    def __str__(self):
        return f"{self.policy.name} - v{self.version_number}"
