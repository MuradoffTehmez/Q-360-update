from django.db import models
from apps.core.models import TimeStampedModel

class FeatureFlag(TimeStampedModel):
    name = models.CharField('Bayraq adı', max_length=100, unique=True, help_text="Xüsusiyyət bayrağı üçün unikal kod adı, məsələn: AI_SCREENING")
    description = models.TextField('Açıqlama', blank=True)
    is_active = models.BooleanField('Aktivdir', default=False)
    percentage_rollout = models.PositiveSmallIntegerField('Yayılma faizi', default=100, help_text="İstifadəçilərin neçə faizinə tətbiq olunacaq (0-100)")
    
    class Meta:
        verbose_name = 'Xüsusiyyət Bayrağı'
        verbose_name_plural = 'Xüsusiyyət Bayraqları'

    def __str__(self):
        status = 'AÇIQ' if self.is_active else 'BAĞLI'
        return f"{self.name} ({status})"

class FeatureFlagRule(TimeStampedModel):
    flag = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE, related_name='rules', verbose_name='Bayraq')
    target_users = models.JSONField('Hədəf istifadəçilər', blank=True, null=True, help_text="Bu bayrağın xüsusi olaraq aktiv olacağı İstifadəçi ID-lərinin siyahısı. Məsələn: [1, 2, 5]", default=list)
    target_departments = models.JSONField('Hədəf departamentlər', blank=True, null=True, help_text="Departament ID-lərinin siyahısı. Məsələn: [3, 7]", default=list)

    class Meta:
        verbose_name = 'Bayraq Qaydası'
        verbose_name_plural = 'Bayraq Qaydaları'

    def __str__(self):
        return f"{self.flag.name} üçün qayda"


class Environment(TimeStampedModel):
    name = models.CharField('Mühit adı', max_length=50, unique=True, help_text="Məsələn: Development, Staging, Production")
    description = models.TextField('Açıqlama', blank=True)
    is_active = models.BooleanField('Aktivdir', default=True)

    class Meta:
        verbose_name = 'Mühit (Environment)'
        verbose_name_plural = 'Mühitlər'

    def __str__(self):
        return self.name


class RolloutStrategy(TimeStampedModel):
    flag = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE, related_name='rollout_strategies', verbose_name='Bayraq')
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE, related_name='rollout_strategies', verbose_name='Mühit')
    strategy_type = models.CharField('Strategiya', max_length=50, choices=[('PERCENTAGE', 'Faizlə Yayılma'), ('TARGETED', 'Hədəf Qrupu')], default='PERCENTAGE')
    percentage = models.PositiveSmallIntegerField('Faiz', default=0)
    
    class Meta:
        verbose_name = 'Yayılma Strategiyası'
        verbose_name_plural = 'Yayılma Strategiyaları'
        unique_together = ('flag', 'environment')

    def __str__(self):
        return f"{self.flag.name} - {self.environment.name}"


class Experiment(TimeStampedModel):
    name = models.CharField('Eksperiment', max_length=255)
    flag = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE, related_name='experiments', verbose_name='Bayraq')
    start_date = models.DateTimeField('Başlanğıc')
    end_date = models.DateTimeField('Bitmə', null=True, blank=True)
    status = models.CharField('Status', max_length=50, choices=[('RUNNING', 'Davam Edir'), ('PAUSED', 'Dayandırılıb'), ('FINISHED', 'Bitdi')], default='RUNNING')
    metrics_json = models.JSONField('Metriklər (JSON)', default=dict, blank=True)

    class Meta:
        verbose_name = 'A/B Eksperiment'
        verbose_name_plural = 'A/B Eksperimentlər'

    def __str__(self):
        return self.name


class FeatureFlagLog(TimeStampedModel):
    flag = models.ForeignKey(FeatureFlag, on_delete=models.CASCADE, related_name='logs', verbose_name='Bayraq')
    action = models.CharField('Əməliyyat', max_length=100)
    actor = models.CharField('İcraçı', max_length=100)
    details = models.JSONField('Detallar', default=dict, blank=True)

    class Meta:
        verbose_name = 'Bayraq Jurnalı'
        verbose_name_plural = 'Bayraq Jurnalları'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.flag.name} - {self.action}"

