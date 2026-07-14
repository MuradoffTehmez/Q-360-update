"""
Models for competencies app - Kompetensiya və Vəzifə İdarəetməsi.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class Competency(models.Model):
    """
    Kompetensiya Bankı - Təşkilat üçün əsas bacarıq və kompetensiyalar.
    Qiymətləndirmə sualları, inkişaf planları və vəzifələrlə əlaqələndirilir.
    """

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_('Kompetensiya Adı')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Aktiv')
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    # Simple History for audit trail
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Kompetensiya')
        verbose_name_plural = _('Kompetensiyalar')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
            models.Index(fields=['name', 'is_active']),  # For combined filtering
        ]

    def __str__(self):
        return self.name

    def get_active_positions(self):
        """Aktiv vəzifələri qaytarır."""
        return self.position_competencies.filter(
            position__is_active=True
        ).select_related('position')

    def get_total_users_with_skill(self):
        """Bu kompetensiyaya malik istifadəçi sayını qaytarır."""
        return self.user_skills.filter(
            is_approved=True,
            user__is_active=True
        ).count()


class ProficiencyLevel(models.Model):
    """
    Kompetensiya Səviyyələri (məsələn: Əsas, Orta, Ekspert).
    Hər səviyyə minimum və maksimum bal aralığı ilə müəyyən edilir.
    """

    LEVEL_CHOICES = [
        ('basic', 'Əsas'),
        ('intermediate', 'Orta'),
        ('advanced', 'Təkmil'),
        ('expert', 'Ekspert'),
    ]

    name = models.CharField(
        max_length=50,
        choices=LEVEL_CHOICES,
        unique=True,
        verbose_name=_('Səviyyə Adı')
    )
    display_name = models.CharField(
        max_length=100,
        verbose_name=_('Göstəriləcək Ad')
    )
    score_min = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Minimum Bal')
    )
    score_max = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Maksimum Bal')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Təsvir')
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    class Meta:
        verbose_name = _('Bacarıq Səviyyəsi')
        verbose_name_plural = _('Bacarıq Səviyyələri')
        ordering = ['score_min']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['score_min', 'score_max']),  # For range queries
        ]

    def __str__(self):
        return f"{self.display_name} ({self.score_min}-{self.score_max})"

    def is_score_in_range(self, score):
        """Verilən balın bu səviyyəyə uyğun olub-olmadığını yoxlayır."""
        return self.score_min <= score <= self.score_max


class PositionCompetency(models.Model):
    """
    Vəzifə-Kompetensiya Əlaqəsi (Many-to-Many).
    Hər vəzifə üçün tələb olunan kompetensiyalar və onların çəkiləri.
    """

    position = models.ForeignKey(
        'departments.Position',
        on_delete=models.CASCADE,
        related_name='position_competencies',
        verbose_name=_('Vəzifə')
    )
    competency = models.ForeignKey(
        Competency,
        on_delete=models.CASCADE,
        related_name='position_competencies',
        verbose_name=_('Kompetensiya')
    )
    weight = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        default=50,
        verbose_name=_('Çəki (%)'),
        help_text=_('Bu kompetensiyanın vəzifə üçün əhəmiyyət dərəcəsi (1-100%)')
    )
    required_level = models.ForeignKey(
        ProficiencyLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='position_requirements',
        verbose_name=_('Tələb Olunan Səviyyə')
    )
    is_mandatory = models.BooleanField(
        default=True,
        verbose_name=_('Məcburi'),
        help_text=_('Bu kompetensiya vəzifə üçün məcburidirmi?')
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    # Simple History
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Vəzifə Kompetensiyası')
        verbose_name_plural = _('Vəzifə Kompetensiyaları')
        unique_together = [['position', 'competency']]
        ordering = ['-weight', 'competency__name']
        indexes = [
            models.Index(fields=['position', 'weight']),
            models.Index(fields=['competency']),
        ]

    def __str__(self):
        return f"{self.position.title} - {self.competency.name} ({self.weight}%)"

    def clean(self):
        """Validation for weight and other constraints."""
        from django.core.exceptions import ValidationError

        # Ensure weight is between 1 and 100
        if self.weight < 1 or self.weight > 100:
            raise ValidationError({
                'weight': _('Çəki 1 ilə 100 arasında olmalıdır.')
            })


class UserSkill(models.Model):
    """
    İstifadəçinin Fərdi Bacarıq Qeydləri.
    İstifadəçilər öz bacarıqlarını qeyd edə və menecerlər təsdiq edə bilər.
    """

    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('approved', 'Təsdiqləndi'),
        ('rejected', 'Rədd Edildi'),
    ]

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='user_skills',
        verbose_name=_('İstifadəçi')
    )
    competency = models.ForeignKey(
        Competency,
        on_delete=models.CASCADE,
        related_name='user_skills',
        verbose_name=_('Kompetensiya')
    )
    level = models.ForeignKey(
        ProficiencyLevel,
        on_delete=models.CASCADE,
        related_name='user_skills',
        verbose_name=_('Səviyyə')
    )
    current_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Cari Bal'),
        help_text=_('Qiymətləndirmədən əldə edilən son bal')
    )

    # Approval workflow
    is_approved = models.BooleanField(
        default=False,
        verbose_name=_('Təsdiqləndi')
    )
    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        default='pending',
        verbose_name=_('Təsdiq Statusu')
    )
    approved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_skills',
        verbose_name=_('Təsdiqləyən')
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Təsdiq Tarixi')
    )

    # Self-assessment
    self_assessment_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Özünüqiymətləndirmə Balı')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    # Simple History
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('İstifadəçi Bacarığı')
        verbose_name_plural = _('İstifadəçi Bacarıqları')
        unique_together = [['user', 'competency']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_approved']),
            models.Index(fields=['competency', 'level']),
            models.Index(fields=['approval_status']),
            models.Index(fields=['user', 'competency', 'is_approved']),  # For combined filtering
            models.Index(fields=['current_score']),  # For score-based queries
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.competency.name} ({self.level.display_name})"

    def approve(self, approver):
        """Bacarığı təsdiq et."""
        from django.utils import timezone
        self.is_approved = True
        self.approval_status = 'approved'
        self.approved_by = approver
        self.approved_at = timezone.now()
        self.save()

    def reject(self, approver):
        """Bacarığı rədd et."""
        from django.utils import timezone
        self.is_approved = False
        self.approval_status = 'rejected'
        self.approved_by = approver
        self.approved_at = timezone.now()
        self.save()

    def update_score_from_evaluation(self, evaluation_score):
        """Qiymətləndirmədən gələn balı yenilə."""
        self.current_score = evaluation_score

        # Automatically update level based on score
        try:
            matching_level = ProficiencyLevel.objects.filter(
                score_min__lte=evaluation_score,
                score_max__gte=evaluation_score
            ).first()

            if matching_level:
                self.level = matching_level
        except ProficiencyLevel.DoesNotExist:
            pass

        self.save()

    def get_proficiency_score(self):
        """Convert proficiency level to numeric score (0-100) for charts."""
        if self.current_score:
            return float(self.current_score)

        # If no current score, use level midpoint
        if self.level:
            midpoint = (float(self.level.score_min) + float(self.level.score_max)) / 2
            return round(midpoint, 1)

        # Default fallback
        level_map = {
            'basic': 25.0,
            'intermediate': 50.0,
            'advanced': 75.0,
            'expert': 95.0
        }
        if self.level and hasattr(self.level, 'name'):
            return level_map.get(self.level.name, 50.0)
        return 50.0

    @property
    def proficiency_level(self):
        """Return proficiency level name."""
        if self.level:
            return self.level.display_name
        return "Naməlum"


class BehavioralIndicator(models.Model):
    """
    Davranış İndikatorları.
    Müəyyən bir kompetensiyanın konkret səviyyəsində gözlənilən davranışlar.
    """
    competency = models.ForeignKey(
        Competency,
        on_delete=models.CASCADE,
        related_name='behaviors',
        verbose_name=_('Kompetensiya')
    )
    level = models.ForeignKey(
        ProficiencyLevel,
        on_delete=models.CASCADE,
        related_name='behaviors',
        verbose_name=_('Səviyyə')
    )
    description = models.TextField(verbose_name=_('Davranış Təsviri'))
    is_active = models.BooleanField(default=True, verbose_name=_('Aktivdir'))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Davranış İndikatoru')
        verbose_name_plural = _('Davranış İndikatorları')
        ordering = ['competency', 'level']

    def __str__(self):
        return f"{self.competency.name} ({self.level.display_name})"

