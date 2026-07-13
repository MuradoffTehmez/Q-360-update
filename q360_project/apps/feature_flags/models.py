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
