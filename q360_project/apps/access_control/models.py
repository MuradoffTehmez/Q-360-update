from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel, SoftDeletableModel

class Role(TimeStampedModel, SoftDeletableModel):
    name = models.CharField('Rol adı', max_length=255, unique=True)
    description = models.TextField('Açıqlama', blank=True)
    is_system = models.BooleanField('Sistem roludur', default=False)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Rollar'

    def __str__(self):
        return self.name

class Permission(TimeStampedModel):
    code = models.CharField('İcazə kodu', max_length=255, unique=True, help_text="Məsələn: workflow:create, leave:approve")
    description = models.TextField('Açıqlama', blank=True)
    module = models.CharField('Modul', max_length=100, help_text="İcazənin aid olduğu modul adı")

    class Meta:
        verbose_name = 'İcazə'
        verbose_name_plural = 'İcazələr'

    def __str__(self):
        return self.code

class RolePermission(TimeStampedModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions', verbose_name='Rol')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='İcazə')

    class Meta:
        verbose_name = 'Rol İcazəsi'
        verbose_name_plural = 'Rol İcazələri'
        unique_together = ('role', 'permission')

class UserRole(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='roles', verbose_name='İstifadəçi')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='Rol')

    class Meta:
        verbose_name = 'İstifadəçi Rolu'
        verbose_name_plural = 'İstifadəçi Rolları'
        unique_together = ('user', 'role')

class AbacPolicy(TimeStampedModel, SoftDeletableModel):
    name = models.CharField('Siyasət adı', max_length=255)
    description = models.TextField('Açıqlama', blank=True)
    resource = models.CharField('Resurs', max_length=255, help_text="Siyasətin tətbiq olunduğu resurs, məsələn: LeaveRequest")
    action = models.CharField('Əməliyyat', max_length=100, help_text="Əməliyyat növü, məsələn: approve, read, update")
    condition_json = models.JSONField('Şərt qaydaları (JSON)', help_text="JSONLogic formatında şərt qaydalarını daxil edin. Məsələn: {\"==\": [{\"var\": \"department\"}, \"IT\"]}", default=dict, blank=True)

    class Meta:
        verbose_name = 'ABAC Siyasəti'
        verbose_name_plural = 'ABAC Siyasətləri'

    def __str__(self):
        return f"{self.action} → {self.resource}"
