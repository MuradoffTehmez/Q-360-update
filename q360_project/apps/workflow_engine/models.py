from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from apps.core.models import TimeStampedModel, SoftDeletableModel

class WorkflowTemplate(TimeStampedModel, SoftDeletableModel):
    name = models.CharField('Şablon adı', max_length=255)
    description = models.TextField('Açıqlama', blank=True)
    is_active = models.BooleanField('Aktivdir', default=True)

    class Meta:
        verbose_name = 'İş Axını Şablonu'
        verbose_name_plural = 'İş Axını Şablonları'

    def __str__(self):
        return self.name

class WorkflowStep(TimeStampedModel):
    STEP_TYPE_CHOICES = (
        ('APPROVAL', 'Təsdiq'),
        ('AUTOMATIC_TASK', 'Avtomatik tapşırıq'),
        ('NOTIFICATION', 'Bildiriş'),
        ('CONDITION', 'Şərt yoxlama'),
    )
    template = models.ForeignKey(WorkflowTemplate, on_delete=models.CASCADE, related_name='steps', verbose_name='Şablon')
    name = models.CharField('Addımın adı', max_length=255)
    description = models.TextField('Açıqlama', blank=True)
    step_order = models.PositiveIntegerField('Sıra nömrəsi')
    step_type = models.CharField('Addım növü', max_length=50, choices=STEP_TYPE_CHOICES, default='APPROVAL')

    class Meta:
        verbose_name = 'İş Axını Addımı'
        verbose_name_plural = 'İş Axını Addımları'
        ordering = ['step_order']

    def __str__(self):
        return f"{self.template.name} - {self.name}"

class WorkflowCondition(TimeStampedModel):
    name = models.CharField('Şərt adı', max_length=255)
    rule_json = models.JSONField('Şərt qaydaları (JSON)', help_text="Şərt qaydalarını JSON formatında daxil edin. Məsələn: {\"==\": [{\"var\": \"department\"}, \"IT\"]}", default=dict, blank=True)

    class Meta:
        verbose_name = 'İş Axını Şərti'
        verbose_name_plural = 'İş Axını Şərtləri'

    def __str__(self):
        return self.name

class WorkflowTransition(TimeStampedModel):
    source_step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE, related_name='outgoing_transitions', verbose_name='Çıxış addımı')
    destination_step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE, related_name='incoming_transitions', null=True, blank=True, verbose_name='Hədəf addımı')
    condition = models.ForeignKey(WorkflowCondition, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Şərt')

    class Meta:
        verbose_name = 'İş Axını Keçidi'
        verbose_name_plural = 'İş Axını Keçidləri'

    def __str__(self):
        dest = self.destination_step.name if self.destination_step else "SON"
        return f"{self.source_step.name} → {dest}"

class WorkflowInstance(TimeStampedModel, SoftDeletableModel):
    STATUS_CHOICES = (
        ('PENDING', 'Gözləyir'),
        ('IN_PROGRESS', 'Davam edir'),
        ('COMPLETED', 'Tamamlandı'),
        ('REJECTED', 'Rədd edildi'),
        ('CANCELLED', 'Ləğv edildi'),
    )
    template = models.ForeignKey(WorkflowTemplate, on_delete=models.PROTECT, related_name='instances', verbose_name='Şablon')
    status = models.CharField('Status', max_length=50, choices=STATUS_CHOICES, default='PENDING')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='requested_workflows', verbose_name='Müraciət edən')
    
    # Generic relation to target object (e.g., LeaveRequest)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Məzmun tipi')
    object_id = models.PositiveIntegerField('Obyekt ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'İş Axını İnstansiyası'
        verbose_name_plural = 'İş Axını İnstansiyaları'

    def __str__(self):
        return f"{self.template.name} - {self.get_status_display()}"

class WorkflowInstanceStep(TimeStampedModel):
    STATUS_CHOICES = (
        ('PENDING', 'Gözləyir'),
        ('APPROVED', 'Təsdiqləndi'),
        ('REJECTED', 'Rədd edildi'),
        ('SKIPPED', 'Keçildi'),
    )
    instance = models.ForeignKey(WorkflowInstance, on_delete=models.CASCADE, related_name='active_steps', verbose_name='İnstansiya')
    step = models.ForeignKey(WorkflowStep, on_delete=models.PROTECT, verbose_name='Addım')
    status = models.CharField('Status', max_length=50, choices=STATUS_CHOICES, default='PENDING')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Təyin olunan')

    class Meta:
        verbose_name = 'İnstansiya Addımı'
        verbose_name_plural = 'İnstansiya Addımları'

    def __str__(self):
        return f"{self.instance} - {self.step.name} ({self.get_status_display()})"

class WorkflowHistory(TimeStampedModel):
    instance = models.ForeignKey(WorkflowInstance, on_delete=models.CASCADE, related_name='history', verbose_name='İnstansiya')
    step = models.ForeignKey(WorkflowStep, on_delete=models.SET_NULL, null=True, verbose_name='Addım')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='İcraçı')
    action = models.CharField('Əməliyyat', max_length=100)
    comments = models.TextField('Şərhlər', blank=True)

    class Meta:
        verbose_name = 'İş Axını Tarixi'
        verbose_name_plural = 'İş Axını Tarixçəsi'

    def __str__(self):
        return f"{self.instance} - {self.action} ({self.actor})"
