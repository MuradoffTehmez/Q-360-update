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


class UserGroup(TimeStampedModel, SoftDeletableModel):
    name = models.CharField('Qrup adı', max_length=255, unique=True)
    description = models.TextField('Açıqlama', blank=True)
    roles = models.ManyToManyField(Role, related_name='groups', blank=True, verbose_name='Rollar')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='access_groups', blank=True, verbose_name='İstifadəçilər')

    class Meta:
        verbose_name = 'İstifadəçi Qrupu'
        verbose_name_plural = 'İstifadəçi Qrupları'

    def __str__(self):
        return self.name


class AccessRequest(TimeStampedModel):
    STATUS_CHOICES = (
        ('PENDING', 'Gözləyir'),
        ('APPROVED', 'Təsdiqləndi'),
        ('REJECTED', 'Rədd edildi'),
    )
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='access_requests_sent', verbose_name='Müraciət edən')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tələb olunan Rol')
    permission = models.ForeignKey(Permission, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Tələb olunan İcazə')
    reason = models.TextField('Səbəb')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='PENDING')
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='access_requests_approved', verbose_name='Təsdiqləyən')

    class Meta:
        verbose_name = 'Giriş İcazəsi Müraciəti'
        verbose_name_plural = 'Giriş İcazəsi Müraciətləri'

    def __str__(self):
        return f"{self.requester} - {self.status}"


class AccessHistory(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='access_history', verbose_name='İstifadəçi')
    action = models.CharField('Əməliyyat', max_length=100)
    resource = models.CharField('Resurs', max_length=255)
    ip_address = models.GenericIPAddressField('IP Ünvanı', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True)
    status = models.CharField('Status', max_length=50, default='SUCCESS')

    class Meta:
        verbose_name = 'Giriş Tarixçəsi'
        verbose_name_plural = 'Giriş Tarixçələri'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.action} on {self.resource}"

