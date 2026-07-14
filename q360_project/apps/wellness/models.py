"""
Models for Wellness & Well-Being module.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from simple_history.models import HistoricalRecords
from apps.accounts.models import User


class HealthCheckup(models.Model):
    """
    Tibbi müayinə planlaması və qeydləri.
    Medical checkup scheduling and records.
    """
    STATUS_CHOICES = [
        ('scheduled', 'Planlaşdırılıb'),
        ('completed', 'Tamamlanıb'),
        ('cancelled', 'Ləğv edilib'),
        ('missed', 'Buraxılıb'),
    ]

    CHECKUP_TYPE_CHOICES = [
        ('general', 'Ümumi Müayinə'),
        ('dental', 'Diş Müayinəsi'),
        ('vision', 'Göz Müayinəsi'),
        ('blood_test', 'Qan Testi'),
        ('cardiology', 'Kardioloji Müayinə'),
        ('annual', 'İllik Müayinə'),
        ('other', 'Digər'),
    ]

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='health_checkups',
        verbose_name=_('İşçi')
    )
    checkup_type = models.CharField(
        max_length=50,
        choices=CHECKUP_TYPE_CHOICES,
        verbose_name=_('Müayinə Növü')
    )
    scheduled_date = models.DateTimeField(
        verbose_name=_('Planlaşdırılmış Tarix')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        verbose_name=_('Status')
    )
    provider = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Tibbi Xidmət Təminatçısı')
    )
    location = models.CharField(
        max_length=300,
        blank=True,
        verbose_name=_('Yer')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )
    results = models.TextField(
        blank=True,
        verbose_name=_('Nəticələr')
    )
    completed_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Tamamlanma Tarixi')
    )
    reminder_sent = models.BooleanField(
        default=False,
        verbose_name=_('Xatırlatma Göndərilib')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Tibbi Müayinə')
        verbose_name_plural = _('Tibbi Müayinələr')
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.get_checkup_type_display()} ({self.scheduled_date.strftime('%Y-%m-%d')})"


class MentalHealthSurvey(models.Model):
    """
    Mental sağlamlıq və stress səviyyəsi survey-ləri.
    Mental health and stress level surveys.
    """
    STRESS_LEVEL_CHOICES = [
        (1, 'Çox Aşağı'),
        (2, 'Aşağı'),
        (3, 'Orta'),
        (4, 'Yüksək'),
        (5, 'Çox Yüksək'),
    ]

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mental_health_surveys',
        verbose_name=_('İşçi')
    )
    survey_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Survey Tarixi')
    )
    stress_level = models.IntegerField(
        choices=STRESS_LEVEL_CHOICES,
        verbose_name=_('Stress Səviyyəsi')
    )
    workload_satisfaction = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('İş Yükü Məmnuniyyəti (1-5)')
    )
    work_life_balance = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('İş-Həyat Balansı (1-5)')
    )
    sleep_quality = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Yuxu Keyfiyyəti (1-5)')
    )
    anxiety_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Narahatlıq Səviyyəsi (1-5)')
    )
    seeking_support = models.BooleanField(
        default=False,
        verbose_name=_('Dəstək Axtarır')
    )
    comments = models.TextField(
        blank=True,
        verbose_name=_('Şərhlər')
    )
    is_anonymous = models.BooleanField(
        default=True,
        verbose_name=_('Anonim Survey')
    )
    follow_up_required = models.BooleanField(
        default=False,
        verbose_name=_('Növbəti Addım Tələb olunur')
    )
    follow_up_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Növbəti Addım Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Mental Sağlamlıq Survey')
        verbose_name_plural = _('Mental Sağlamlıq Survey-ləri')
        ordering = ['-survey_date']

    def __str__(self):
        return f"{self.employee.get_full_name() if not self.is_anonymous else 'Anonim'} - {self.survey_date}"

    def get_overall_score(self):
        """Ümumi mental sağlamlıq skoru hesabla (0-100)"""
        # Stress və anxiety-ni tərsinə çeviririk (yüksək dəyər = pis)
        stress_score = (6 - self.stress_level) * 20
        anxiety_score = (6 - self.anxiety_level) * 20
        # Müsbət göstəriciləri hesablayırıq
        workload_score = self.workload_satisfaction * 20
        balance_score = self.work_life_balance * 20
        sleep_score = self.sleep_quality * 20

        # Ortalama
        return (stress_score + anxiety_score + workload_score + balance_score + sleep_score) / 5


class FitnessProgram(models.Model):
    """
    Fitness proqramları və idman fəaliyyətləri.
    Fitness programs and sports activities.
    """
    STATUS_CHOICES = [
        ('active', 'Aktiv'),
        ('upcoming', 'Gələcək'),
        ('completed', 'Tamamlanıb'),
        ('cancelled', 'Ləğv edilib'),
    ]

    PROGRAM_TYPE_CHOICES = [
        ('gym', 'Fitness Zalı'),
        ('yoga', 'Yoga'),
        ('pilates', 'Pilates'),
        ('running', 'Qaçış Qrupu'),
        ('cycling', 'Velosiped'),
        ('swimming', 'Üzgüçülük'),
        ('team_sports', 'Komanda İdmanı'),
        ('wellness', 'Wellness Proqramı'),
        ('other', 'Digər'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name=_('Proqram Adı')
    )
    description = models.TextField(
        verbose_name=_('Təsvir')
    )
    program_type = models.CharField(
        max_length=50,
        choices=PROGRAM_TYPE_CHOICES,
        verbose_name=_('Proqram Növü')
    )
    start_date = models.DateField(
        verbose_name=_('Başlama Tarixi')
    )
    end_date = models.DateField(
        verbose_name=_('Bitmə Tarixi')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='upcoming',
        verbose_name=_('Status')
    )
    capacity = models.IntegerField(
        default=20,
        verbose_name=_('Maksimum İştirakçı Sayı')
    )
    participants = models.ManyToManyField(
        User,
        related_name='fitness_programs',
        blank=True,
        verbose_name=_('İştirakçılar')
    )
    instructor = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Təlimatçı')
    )
    location = models.CharField(
        max_length=300,
        verbose_name=_('Yer')
    )
    schedule = models.TextField(
        blank=True,
        verbose_name=_('Cədvəl')
    )
    cost_per_person = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Nəfər Başı Qiymət')
    )
    company_sponsored = models.BooleanField(
        default=True,
        verbose_name=_('Şirkət Tərəfindən Dəstəklənir')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Fitness Proqramı')
        verbose_name_plural = _('Fitness Proqramları')
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} ({self.start_date})"

    def get_participant_count(self):
        """İştirakçı sayını qaytarır"""
        return self.participants.count()

    def is_full(self):
        """Proqramın dolu olub olmadığını yoxlayır"""
        return self.get_participant_count() >= self.capacity

    def get_available_spots(self):
        """Boş yerlərin sayını qaytarır"""
        return max(0, self.capacity - self.get_participant_count())


class MedicalClaim(models.Model):
    """
    Tibbi xərc tələbləri.
    Medical expense claims.
    """
    STATUS_CHOICES = [
        ('pending', 'Gözləmədə'),
        ('approved', 'Təsdiq edilib'),
        ('rejected', 'Rədd edilib'),
        ('paid', 'Ödənilib'),
    ]

    CLAIM_TYPE_CHOICES = [
        ('consultation', 'Konsultasiya'),
        ('medication', 'Dərman'),
        ('hospitalization', 'Xəstəxana'),
        ('surgery', 'Əməliyyat'),
        ('dental', 'Diş Müalicəsi'),
        ('vision', 'Göz Müalicəsi'),
        ('physical_therapy', 'Fiziki Terapiya'),
        ('mental_health', 'Mental Sağlamlıq'),
        ('other', 'Digər'),
    ]

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='medical_claims',
        verbose_name=_('İşçi')
    )
    claim_type = models.CharField(
        max_length=50,
        choices=CLAIM_TYPE_CHOICES,
        verbose_name=_('Tələb Növü')
    )
    claim_date = models.DateField(
        verbose_name=_('Tələb Tarixi')
    )
    treatment_date = models.DateField(
        verbose_name=_('Müalicə Tarixi')
    )
    provider = models.CharField(
        max_length=200,
        verbose_name=_('Tibbi Xidmət Təminatçısı')
    )
    description = models.TextField(
        verbose_name=_('Təsvir')
    )
    amount_claimed = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('Tələb Edilən Məbləğ')
    )
    amount_approved = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Təsdiq Edilən Məbləğ')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    receipt_file = models.FileField(
        upload_to='medical_claims/receipts/',
        blank=True,
        null=True,
        verbose_name=_('Qəbz Faylı')
    )
    rejection_reason = models.TextField(
        blank=True,
        verbose_name=_('Rədd Səbəbi')
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_medical_claims',
        verbose_name=_('Nəzərdən Keçirən')
    )
    reviewed_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Nəzərdən Keçirmə Tarixi')
    )
    payment_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Ödəniş Tarixi')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Tibbi Xərc Tələbi')
        verbose_name_plural = _('Tibbi Xərc Tələbləri')
        ordering = ['-claim_date']

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.get_claim_type_display()} - {self.amount_claimed}"


class WellnessChallenge(models.Model):
    """
    Wellness yarışları və komanda məşğələləri.
    Wellness challenges and team activities.
    """
    STATUS_CHOICES = [
        ('upcoming', 'Gələcək'),
        ('active', 'Aktiv'),
        ('completed', 'Tamamlanıb'),
        ('cancelled', 'Ləğv edilib'),
    ]

    CHALLENGE_TYPE_CHOICES = [
        ('steps', 'Addım Yarışı'),
        ('hydration', 'Su İçmə Yarışı'),
        ('meditation', 'Meditasiya'),
        ('sleep', 'Yuxu Keyfiyyəti'),
        ('nutrition', 'Sağlam Qidalanma'),
        ('exercise', 'İdman Fəaliyyəti'),
        ('weight_loss', 'Çəki İtirmə'),
        ('other', 'Digər'),
    ]

    title = models.CharField(
        max_length=200,
        verbose_name=_('Yarış Adı')
    )
    description = models.TextField(
        verbose_name=_('Təsvir')
    )
    challenge_type = models.CharField(
        max_length=50,
        choices=CHALLENGE_TYPE_CHOICES,
        verbose_name=_('Yarış Növü')
    )
    start_date = models.DateField(
        verbose_name=_('Başlama Tarixi')
    )
    end_date = models.DateField(
        verbose_name=_('Bitmə Tarixi')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='upcoming',
        verbose_name=_('Status')
    )
    goal = models.CharField(
        max_length=200,
        verbose_name=_('Hədəf')
    )
    prize = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Mükafat')
    )
    participants = models.ManyToManyField(
        User,
        through='WellnessChallengeParticipation',
        related_name='wellness_challenges',
        verbose_name=_('İştirakçılar')
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_challenges',
        verbose_name=_('Yaradan')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Yaradılma Tarixi')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Yenilənmə Tarixi')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Wellness Yarışı')
        verbose_name_plural = _('Wellness Yarışları')
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} ({self.start_date} - {self.end_date})"

    def get_participant_count(self):
        """İştirakçı sayını qaytarır"""
        return self.participants.count()


class WellnessChallengeParticipation(models.Model):
    """
    Wellness yarışlarına iştirak və nəticələr.
    Wellness challenge participation and results.
    """
    challenge = models.ForeignKey(
        WellnessChallenge,
        on_delete=models.CASCADE,
        related_name='participations',
        verbose_name=_('Yarış')
    )
    participant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='challenge_participations',
        verbose_name=_('İştirakçı')
    )
    joined_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Qoşulma Tarixi')
    )
    progress = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_('İrəliləyiş (%)')
    )
    current_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name=_('Cari Dəyər')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )
    completed = models.BooleanField(
        default=False,
        verbose_name=_('Tamamlanıb')
    )
    completion_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Tamamlanma Tarixi')
    )

    class Meta:
        verbose_name = _('Yarış İştirakı')
        verbose_name_plural = _('Yarış İştirakları')
        unique_together = ['challenge', 'participant']
        ordering = ['-progress', '-current_value']

    def __str__(self):
        return f"{self.participant.get_full_name()} - {self.challenge.title}"


class HealthScore(models.Model):
    """
    İşçilərin ümumi sağlamlıq skoru.
    Employee overall health score.
    """
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='health_scores',
        verbose_name=_('İşçi')
    )
    score_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Skor Tarixi')
    )
    overall_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Ümumi Skor (0-100)')
    )
    physical_health = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Fiziki Sağlamlıq')
    )
    mental_health = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Mental Sağlamlıq')
    )
    activity_level = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Aktivlik Səviyyəsi')
    )
    nutrition_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Qidalanma Skoru')
    )
    sleep_quality = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Yuxu Keyfiyyəti')
    )
    bmi = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('BMI (Bədən Kütlə İndeksi)')
    )
    steps_per_day_avg = models.IntegerField(
        default=0,
        verbose_name=_('Gündəlik Ortalama Addım')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Qeydlər')
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Sağlamlıq Skoru')
        verbose_name_plural = _('Sağlamlıq Skorları')
        ordering = ['-score_date']
        unique_together = ['employee', 'score_date']

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.overall_score} ({self.score_date})"

    def calculate_overall_score(self):
        """Ümumi skoru hesabla"""
        scores = [
            self.physical_health,
            self.mental_health,
            self.activity_level,
            self.nutrition_score,
            self.sleep_quality
        ]
        return sum(scores) / len(scores)

    def get_bmi_category(self):
        """BMI kateqoriyasını qaytarır"""
        if not self.bmi:
            return "Məlumat yoxdur"

        if self.bmi < 18.5:
            return "Arıq"
        elif 18.5 <= self.bmi < 25:
            return "Normal"
        elif 25 <= self.bmi < 30:
            return "Artıq Çəki"
        else:
            return "Piylənmə"


class StepTracking(models.Model):
    """
    Gündəlik addım sayğacı məlumatları.
    Daily step tracking data.
    """
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='step_trackings',
        verbose_name=_('İşçi')
    )
    tracking_date = models.DateField(
        verbose_name=_('Tarix')
    )
    steps = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_('Addım Sayı')
    )
    distance_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,
        verbose_name=_('Məsafə (km)')
    )
    calories_burned = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_('Yandırılan Kalori')
    )
    active_minutes = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_('Aktiv Dəqiqələr')
    )
    data_source = models.CharField(
        max_length=50,
        default='manual',
        verbose_name=_('Məlumat Mənbəyi')
    )
    synced_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Sinxronizasiya Tarixi')
    )

    class Meta:
        verbose_name = _('Addım İzləmə')
        verbose_name_plural = _('Addım İzləmələri')
        ordering = ['-tracking_date']
        unique_together = ['employee', 'tracking_date']

    def __str__(self):
        return f"{self.employee.get_full_name()} - {self.steps} addım ({self.tracking_date})"


class Benefit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wellness_benefits')
    name = models.CharField(_('Müavinət/Sığorta Adı'), max_length=200)
    provider = models.CharField(_('Təminatçı'), max_length=100)
    coverage_details = models.TextField(_('Əhatə Dairəsi'), blank=True)
    start_date = models.DateField(_('Başlanğıc Tarixi'))
    end_date = models.DateField(_('Bitmə Tarixi'), null=True, blank=True)
    is_active = models.BooleanField(_('Aktivdir'), default=True)

    class Meta:
        verbose_name = _('Müavinət/Sığorta')
        verbose_name_plural = _('Müavinətlər')

class HealthGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_goals')
    title = models.CharField(_('Hədəf Adı'), max_length=200)
    description = models.TextField(_('Təsvir'), blank=True)
    target_date = models.DateField(_('Hədəf Tarixi'))
    status = models.CharField(max_length=20, choices=[('active', 'Aktiv'), ('completed', 'Tamamlandı'), ('abandoned', 'Dayandırıldı')], default='active')

    class Meta:
        verbose_name = _('Sağlamlıq Hədəfi')
        verbose_name_plural = _('Sağlamlıq Hədəfləri')

class VaccinationRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine_name = models.CharField(_('Peyvənd Adı'), max_length=100)
    dose_number = models.IntegerField(_('Doza Nömrəsi'), default=1)
    administered_date = models.DateField(_('Vurulma Tarixi'))
    next_due_date = models.DateField(_('Növbəti Doza Tarixi'), null=True, blank=True)
    notes = models.TextField(_('Qeydlər'), blank=True)

    class Meta:
        verbose_name = _('Peyvənd Qeydi')
        verbose_name_plural = _('Peyvənd Qeydləri')

