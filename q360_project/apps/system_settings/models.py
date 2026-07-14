"""
System Settings models.
Platform-wide configuration stored as categorized key/value pairs.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.core.models import TimeStampedModel


class SystemSetting(TimeStampedModel):
    """A single configuration entry belonging to a settings category."""

    VALUE_TYPES = [
        ('text', _('Mətn')),
        ('int', _('Tam ədəd')),
        ('bool', _('Bəli/Xeyr')),
        ('json', _('JSON')),
    ]

    category = models.SlugField(
        max_length=50,
        db_index=True,
        verbose_name=_('Kateqoriya')
    )
    key = models.CharField(
        max_length=100,
        verbose_name=_('Açar')
    )
    value = models.TextField(
        blank=True,
        verbose_name=_('Dəyər')
    )
    value_type = models.CharField(
        max_length=10,
        choices=VALUE_TYPES,
        default='text',
        verbose_name=_('Dəyər tipi')
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Təsvir')
    )
    is_sensitive = models.BooleanField(
        default=False,
        verbose_name=_('Həssas məlumat'),
        help_text=_('Həssas dəyərlər UI-də maskalanır.')
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_settings',
        verbose_name=_('Yeniləyən')
    )

    class Meta:
        verbose_name = _('Sistem Parametri')
        verbose_name_plural = _('Sistem Parametrləri')
        unique_together = [['category', 'key']]
        ordering = ['category', 'key']

    def __str__(self):
        return f'{self.category}.{self.key}'

    @property
    def display_value(self):
        if self.is_sensitive and self.value:
            return '••••••••'
        return self.value
