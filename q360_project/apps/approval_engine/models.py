from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.core.models import TimeStampedModel, SoftDeletableModel

class ApprovalChain(TimeStampedModel, SoftDeletableModel):
    name = models.CharField('Zəncir adı', max_length=255)
    description = models.TextField('Açıqlama', blank=True)
    is_active = models.BooleanField('Aktivdir', default=True)

    class Meta:
        verbose_name = 'Təsdiq Zənciri'
        verbose_name_plural = 'Təsdiq Zəncirləri'

    def __str__(self):
        return self.name

class ApprovalRule(TimeStampedModel):
    chain = models.ForeignKey(ApprovalChain, on_delete=models.CASCADE, related_name='rules', verbose_name='Zəncir')
    name = models.CharField('Qayda adı', max_length=255)
    condition_json = models.JSONField('Şərtlər (JSON)', default=dict, blank=True)
    is_active = models.BooleanField('Aktivdir', default=True)

    class Meta:
        verbose_name = 'Təsdiq Qaydası'
        verbose_name_plural = 'Təsdiq Qaydaları'

    def __str__(self):
        return f"{self.chain.name} - {self.name}"

class ApprovalNode(TimeStampedModel):
    NODE_TYPE_CHOICES = (
        ('USER', 'Konkret İstifadəçi'),
        ('ROLE', 'Konkret Rol'),
        ('MANAGER', 'Birbaşa Rəhbər'),
        ('DYNAMIC', 'Dinamik Şərt'),
    )
    chain = models.ForeignKey(ApprovalChain, on_delete=models.CASCADE, related_name='nodes', verbose_name='Zəncir')
    node_type = models.CharField('Qovşaq növü', max_length=50, choices=NODE_TYPE_CHOICES)
    approver_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Təsdiq edən istifadəçi')
    order = models.PositiveIntegerField('Sıra nömrəsi')

    class Meta:
        verbose_name = 'Təsdiq Qovşağı'
        verbose_name_plural = 'Təsdiq Qovşaqları'
        ordering = ['order']

    def __str__(self):
        return f"{self.chain.name} - Addım {self.order}"

class ApprovalRequest(TimeStampedModel):
    STATUS_CHOICES = (
        ('PENDING', 'Gözləyir'),
        ('APPROVED', 'Təsdiqləndi'),
        ('REJECTED', 'Rədd edildi'),
    )
    chain = models.ForeignKey(ApprovalChain, on_delete=models.PROTECT, verbose_name='Zəncir')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='approval_requests', verbose_name='Müraciət edən')
    status = models.CharField('Status', max_length=50, choices=STATUS_CHOICES, default='PENDING')
    current_node = models.ForeignKey(ApprovalNode, on_delete=models.SET_NULL, null=True, verbose_name='Cari qovşaq')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Məzmun tipi')
    object_id = models.PositiveIntegerField('Obyekt ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Təsdiq Müraciəti'
        verbose_name_plural = 'Təsdiq Müraciətləri'

    def __str__(self):
        return f"{self.chain.name} - {self.requester} ({self.get_status_display()})"

class ApprovalDelegation(TimeStampedModel):
    delegator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delegations_given', verbose_name='Səlahiyyət verən')
    delegatee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delegations_received', verbose_name='Səlahiyyət alan')
    start_date = models.DateTimeField('Başlanğıc tarixi')
    end_date = models.DateTimeField('Bitmə tarixi')
    is_active = models.BooleanField('Aktivdir', default=True)

    class Meta:
        verbose_name = 'Təsdiq Delegasiyası'
        verbose_name_plural = 'Təsdiq Delegasiyaları'

    def __str__(self):
        return f"{self.delegator} → {self.delegatee}"

class ApprovalLog(TimeStampedModel):
    request = models.ForeignKey(ApprovalRequest, on_delete=models.CASCADE, related_name='logs', verbose_name='Müraciət')
    node = models.ForeignKey(ApprovalNode, on_delete=models.SET_NULL, null=True, verbose_name='Qovşaq')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='İcraçı')
    action = models.CharField('Əməliyyat', max_length=50)
    comments = models.TextField('Şərhlər', blank=True)

    class Meta:
        verbose_name = 'Təsdiq Jurnalı'
        verbose_name_plural = 'Təsdiq Jurnalları'

    def __str__(self):
        return f"{self.request} - {self.action} ({self.actor})"
