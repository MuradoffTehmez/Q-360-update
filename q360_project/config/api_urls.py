"""
API URL configuration for Q360 Evaluation System.
All DRF API endpoints are registered here under /api/ prefix.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import ViewSets
from apps.competencies.views import (
    CompetencyViewSet,
    ProficiencyLevelViewSet,
    PositionCompetencyViewSet,
    UserSkillViewSet,
)
from apps.training.views import (
    TrainingResourceViewSet,
    UserTrainingViewSet,
)
from apps.accounts.views import (
    UserViewSet,
    ProfileViewSet,
    RoleViewSet,
    check_password_strength,
)
from apps.departments.views import (
    OrganizationViewSet,
    DepartmentViewSet,
    PositionViewSet,
)
from apps.engagement.api import (
    PulseSurveyViewSet,
    EngagementScoreViewSet,
    RecognitionViewSet,
    AnonymousFeedbackViewSet,
    LeaderboardViewSet,
    GamificationBadgeViewSet,
    UserBadgeViewSet,
    DashboardViewSet,
)
from apps.compensation.api_views import (
    SalaryInformationViewSet,
    EmployeeBenefitViewSet,
    BonusViewSet,
    CompensationHistoryViewSet,
)
from apps.leave_attendance.api_views import (
    LeaveRequestViewSet,
    AttendanceViewSet,
    LeaveBalanceViewSet,
    LeaveTypeViewSet,
    HolidayViewSet,
)
from apps.recruitment.api_views import (
    JobPostingViewSet,
    ApplicationViewSet,
    InterviewViewSet,
    OfferViewSet,
)
from apps.evaluations.views import (
    EvaluationCampaignViewSet,
    QuestionCategoryViewSet,
    QuestionViewSet,
    EvaluationAssignmentViewSet,
    ResponseViewSet,
    EvaluationResultViewSet,
)
from apps.workforce_planning.views import (
    TalentMatrixViewSet,
    CriticalRoleViewSet,
    SuccessionCandidateViewSet,
    CompetencyGapViewSet,
)
from apps.continuous_feedback.views import (
    QuickFeedbackViewSet,
    FeedbackBankViewSet,
    PublicRecognitionViewSet,
    FeedbackTagViewSet,
    FeedbackStatisticsViewSet,
)
from apps.audit.api_views import (
    AuditLogViewSet,
    BlockedIPViewSet,
)
from apps.dashboard.api_viewsets import (
    SystemKPIViewSet,
    DashboardWidgetViewSet,
    AnalyticsReportViewSet,
    TrendDataViewSet,
    ForecastDataViewSet,
    RealTimeStatViewSet
)
from apps.dashboard import api as dashboard_api
from apps.dashboard import views as dashboard_views
from apps.dashboard import api_views as dashboard_api_views
from apps.development_plans.api_views import (
    DevelopmentGoalViewSet,
    ProgressLogViewSet,
    StrategicObjectiveViewSet,
    KeyResultViewSet,
    KPIViewSet,
    KPIMeasurementViewSet
)
from apps.notifications.api_views import (
    NotificationMethodViewSet,
    NotificationTemplateViewSet,
    NotificationViewSet,
    SMSProviderViewSet,
    SMSLogViewSet,
    SMSNotificationViewSet,
    PushDeviceViewSet,
    PushNotificationViewSet,
    NotificationPreferenceViewSet,
    UserNotificationPreferenceViewSet,
    BulkNotificationViewSet,
    EmailTemplateViewSet,
    EmailLogViewSet,
    EmailNotificationViewSet
)
from apps.sentiment_analysis.api_views import (
    SentimentFeedbackViewSet,
    SentimentAnalysisSettingsViewSet
)
from apps.support.api_views import (
    SupportTicketViewSet,
    TicketCommentViewSet
)
from apps.wellness.api_views import (
    HealthCheckupViewSet,
    MentalHealthSurveyViewSet,
    FitnessProgramViewSet,
    MedicalClaimViewSet,
    WellnessChallengeViewSet,
    WellnessChallengeParticipationViewSet,
    HealthScoreViewSet,
    StepTrackingViewSet
)
from apps.onboarding.api_views import (
    OnboardingTemplateViewSet,
    OnboardingTaskTemplateViewSet,
    OnboardingProcessViewSet,
    OnboardingTaskViewSet,
    OnboardingNoteViewSet,
    MarketSalaryBenchmarkViewSet
)
from apps.performance_reviews.views import ReviewSessionViewSet, ReviewNoteViewSet, ReviewActionItemViewSet, CompetencyEvaluationViewSet
from apps.reports.api_views import (
    ReportViewSet,
    RadarChartDataViewSet,
    ReportGenerationLogViewSet,
    SystemKPIViewSet,
    ReportBlueprintViewSet,
    ReportVisualizationViewSet,
    CustomReportViewSet,
    ReportScheduleViewSet,
    ReportScheduleLogViewSet
)
from apps.search.api_views import search_api_view
from api.real_time_stats import realtime_stats

# Create routers for each app
competencies_router = DefaultRouter()
competencies_router.register(r'competencies', CompetencyViewSet, basename='competency')
competencies_router.register(r'proficiency-levels', ProficiencyLevelViewSet, basename='proficiency-level')
competencies_router.register(r'position-competencies', PositionCompetencyViewSet, basename='position-competency')
competencies_router.register(r'user-skills', UserSkillViewSet, basename='user-skill')

training_router = DefaultRouter()
training_router.register(r'resources', TrainingResourceViewSet, basename='training-resource')
training_router.register(r'user-trainings', UserTrainingViewSet, basename='user-training')

accounts_router = DefaultRouter()
accounts_router.register(r'users', UserViewSet, basename='user')
accounts_router.register(r'profiles', ProfileViewSet, basename='profile')
accounts_router.register(r'roles', RoleViewSet, basename='role')

departments_router = DefaultRouter()
departments_router.register(r'organizations', OrganizationViewSet, basename='organization')
departments_router.register(r'departments', DepartmentViewSet, basename='department')
departments_router.register(r'positions', PositionViewSet, basename='position')

engagement_router = DefaultRouter()
engagement_router.register(r'pulse-surveys', PulseSurveyViewSet, basename='pulse-survey')
engagement_router.register(r'engagement-scores', EngagementScoreViewSet, basename='engagement-score')
engagement_router.register(r'recognitions', RecognitionViewSet, basename='recognition')
engagement_router.register(r'feedback', AnonymousFeedbackViewSet, basename='anonymous-feedback')
engagement_router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
engagement_router.register(r'badges', GamificationBadgeViewSet, basename='badge')
engagement_router.register(r'user-badges', UserBadgeViewSet, basename='user-badge')
engagement_router.register(r'dashboard', DashboardViewSet, basename='engagement-dashboard')

compensation_router = DefaultRouter()
compensation_router.register(r'salary-information', SalaryInformationViewSet, basename='salary-information')
compensation_router.register(r'benefits', EmployeeBenefitViewSet, basename='benefit')
compensation_router.register(r'bonuses', BonusViewSet, basename='bonus')
compensation_router.register(r'compensation-history', CompensationHistoryViewSet, basename='compensation-history')

leave_attendance_router = DefaultRouter()
leave_attendance_router.register(r'leave-requests', LeaveRequestViewSet, basename='leave-request')
leave_attendance_router.register(r'attendance', AttendanceViewSet, basename='attendance')
leave_attendance_router.register(r'leave-balances', LeaveBalanceViewSet, basename='leave-balance')
leave_attendance_router.register(r'leave-types', LeaveTypeViewSet, basename='leave-type')
leave_attendance_router.register(r'holidays', HolidayViewSet, basename='holiday')

recruitment_router = DefaultRouter()
recruitment_router.register(r'job-postings', JobPostingViewSet, basename='job-posting')
recruitment_router.register(r'applications', ApplicationViewSet, basename='application')
recruitment_router.register(r'interviews', InterviewViewSet, basename='interview')
recruitment_router.register(r'offers', OfferViewSet, basename='offer')

# --- NEW: Previously unregistered routers ---

evaluations_router = DefaultRouter()
evaluations_router.register(r'campaigns', EvaluationCampaignViewSet, basename='evaluation-campaign')
evaluations_router.register(r'question-categories', QuestionCategoryViewSet, basename='question-category')
evaluations_router.register(r'questions', QuestionViewSet, basename='question')
evaluations_router.register(r'assignments', EvaluationAssignmentViewSet, basename='assignment')
evaluations_router.register(r'responses', ResponseViewSet, basename='response')
evaluations_router.register(r'results', EvaluationResultViewSet, basename='result')

workforce_router = DefaultRouter()
workforce_router.register(r'talent-matrix', TalentMatrixViewSet, basename='talent-matrix')
workforce_router.register(r'critical-roles', CriticalRoleViewSet, basename='critical-role')
workforce_router.register(r'succession-candidates', SuccessionCandidateViewSet, basename='succession-candidate')
workforce_router.register(r'competency-gaps', CompetencyGapViewSet, basename='competency-gap')

feedback_router = DefaultRouter()
feedback_router.register(r'quick-feedback', QuickFeedbackViewSet, basename='quick-feedback')
feedback_router.register(r'feedback-bank', FeedbackBankViewSet, basename='feedback-bank')
feedback_router.register(r'public-recognition', PublicRecognitionViewSet, basename='public-recognition')
feedback_router.register(r'tags', FeedbackTagViewSet, basename='feedback-tag')
feedback_router.register(r'statistics', FeedbackStatisticsViewSet, basename='feedback-statistics')

audit_router = DefaultRouter()
audit_router.register(r'logs', AuditLogViewSet, basename='audit-log')
audit_router.register(r'blocked-ips', BlockedIPViewSet, basename='blocked-ip')

dashboard_router = DefaultRouter()
dashboard_router.register(r'kpis', SystemKPIViewSet, basename='dashboard-kpi')
dashboard_router.register(r'widgets', DashboardWidgetViewSet, basename='dashboard-widget')
dashboard_router.register(r'reports', AnalyticsReportViewSet, basename='dashboard-report')
dashboard_router.register(r'trends', TrendDataViewSet, basename='dashboard-trend')
dashboard_router.register(r'forecasts', ForecastDataViewSet, basename='dashboard-forecast')
dashboard_router.register(r'stats', RealTimeStatViewSet, basename='dashboard-stat')

dev_plans_router = DefaultRouter()
dev_plans_router.register(r'goals', DevelopmentGoalViewSet, basename='dev-goal')
dev_plans_router.register(r'progress-logs', ProgressLogViewSet, basename='dev-progress')
dev_plans_router.register(r'strategic-objectives', StrategicObjectiveViewSet, basename='dev-objective')
dev_plans_router.register(r'key-results', KeyResultViewSet, basename='dev-keyresult')
dev_plans_router.register(r'kpis', KPIViewSet, basename='dev-kpi')
dev_plans_router.register(r'kpi-measurements', KPIMeasurementViewSet, basename='dev-measurement')

notifications_router = DefaultRouter()
notifications_router.register(r'methods', NotificationMethodViewSet, basename='notification-method')
notifications_router.register(r'templates', NotificationTemplateViewSet, basename='notification-template')
notifications_router.register(r'logs', NotificationViewSet, basename='notification-log')
notifications_router.register(r'sms-providers', SMSProviderViewSet, basename='sms-provider')
notifications_router.register(r'sms-logs', SMSLogViewSet, basename='sms-log')
notifications_router.register(r'sms-notifications', SMSNotificationViewSet, basename='sms-notification')
notifications_router.register(r'push-devices', PushDeviceViewSet, basename='push-device')
notifications_router.register(r'push-notifications', PushNotificationViewSet, basename='push-notification')
notifications_router.register(r'preferences', NotificationPreferenceViewSet, basename='notification-preference')
notifications_router.register(r'user-preferences', UserNotificationPreferenceViewSet, basename='user-notification-preference')
notifications_router.register(r'bulk', BulkNotificationViewSet, basename='bulk-notification')
notifications_router.register(r'email-templates', EmailTemplateViewSet, basename='email-template')
notifications_router.register(r'email-logs', EmailLogViewSet, basename='email-log')
notifications_router.register(r'email-notifications', EmailNotificationViewSet, basename='email-notification')

sentiment_router = DefaultRouter()
sentiment_router.register(r'feedback', SentimentFeedbackViewSet, basename='sentiment-feedback')
sentiment_router.register(r'settings', SentimentAnalysisSettingsViewSet, basename='sentiment-settings')

support_router = DefaultRouter()
support_router.register(r'tickets', SupportTicketViewSet, basename='support-ticket')
support_router.register(r'comments', TicketCommentViewSet, basename='support-comment')

wellness_router = DefaultRouter()
wellness_router.register(r'checkups', HealthCheckupViewSet, basename='wellness-checkup')
wellness_router.register(r'mental-surveys', MentalHealthSurveyViewSet, basename='wellness-survey')
wellness_router.register(r'fitness-programs', FitnessProgramViewSet, basename='wellness-program')
wellness_router.register(r'medical-claims', MedicalClaimViewSet, basename='wellness-claim')
wellness_router.register(r'challenges', WellnessChallengeViewSet, basename='wellness-challenge')
wellness_router.register(r'challenge-participations', WellnessChallengeParticipationViewSet, basename='wellness-participation')
wellness_router.register(r'health-scores', HealthScoreViewSet, basename='wellness-score')
wellness_router.register(r'step-tracking', StepTrackingViewSet, basename='wellness-step')

onboarding_router = DefaultRouter()
onboarding_router.register(r'templates', OnboardingTemplateViewSet, basename='onboarding-template')
onboarding_router.register(r'task-templates', OnboardingTaskTemplateViewSet, basename='onboarding-task-template')
onboarding_router.register(r'processes', OnboardingProcessViewSet, basename='onboarding-process')
onboarding_router.register(r'tasks', OnboardingTaskViewSet, basename='onboarding-task')
onboarding_router.register(r'notes', OnboardingNoteViewSet, basename='onboarding-note')
onboarding_router.register(r'salary-benchmarks', MarketSalaryBenchmarkViewSet, basename='onboarding-salary-benchmark')

performance_reviews_router = DefaultRouter()
performance_reviews_router.register(r'sessions', ReviewSessionViewSet, basename='performance-session')
performance_reviews_router.register(r'notes', ReviewNoteViewSet, basename='performance-note')
performance_reviews_router.register(r'action-items', ReviewActionItemViewSet, basename='performance-action-item')
performance_reviews_router.register(r'competency-evaluations', CompetencyEvaluationViewSet, basename='performance-competency-evaluation')
reports_router = DefaultRouter()
reports_router.register(r'reports', ReportViewSet, basename='report')
reports_router.register(r'radar-charts', RadarChartDataViewSet, basename='report-radar-chart')
reports_router.register(r'generation-logs', ReportGenerationLogViewSet, basename='report-generation-log')
reports_router.register(r'system-kpis', SystemKPIViewSet, basename='report-system-kpi')
reports_router.register(r'blueprints', ReportBlueprintViewSet, basename='report-blueprint')
reports_router.register(r'visualizations', ReportVisualizationViewSet, basename='report-visualization')
reports_router.register(r'custom-reports', CustomReportViewSet, basename='report-custom')
reports_router.register(r'schedules', ReportScheduleViewSet, basename='report-schedule')
reports_router.register(r'schedule-logs', ReportScheduleLogViewSet, basename='report-schedule-log')

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from rest_framework.permissions import AllowAny

# Dashboard extra API endpoints
dashboard_extra_urls = [
    path('stats-summary/', dashboard_api.dashboard_stats, name='api_stats'),
    path('trends-summary/', dashboard_api.dashboard_trends, name='api_trends'),
    path('forecasting-summary/', dashboard_api.dashboard_forecasting, name='api_forecasting'),
    path('realtime-stats-legacy/', dashboard_views.real_time_stats_api, name='realtime_stats_api'),
    path('update-stats/', dashboard_views.update_real_time_stats, name='update_realtime_stats'),
    path('trend/<str:data_type>/', dashboard_views.get_trend_data, name='get_trend_data'),
    path('forecast/<str:forecast_type>/', dashboard_views.get_forecast_data, name='get_forecast_data'),
    path('generate-report/', dashboard_views.generate_analytics_report, name='generate_report'),
    path('data/<str:endpoint>/', dashboard_api_views.dashboard_api_endpoint, name='dashboard_api'),
    path('widget-config/', dashboard_api_views.dashboard_widget_config, name='widget_config'),
    path('department-analytics/', dashboard_api_views.department_analytics, name='department_analytics'),
]

# API URL patterns
urlpatterns = [
    # Swagger / OpenAPI Documentation
    path('schema/', SpectacularAPIView.as_view(permission_classes=[AllowAny]), name='schema'),
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema', permission_classes=[AllowAny]), name='swagger-ui'),
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema', permission_classes=[AllowAny]), name='redoc'),

    path('realtime-stats/', realtime_stats, name='realtime-stats'),
    path('competencies/', include(competencies_router.urls)),
    path('training/', include(training_router.urls)),
    path('accounts/', include(accounts_router.urls)),
    path('accounts/check-password-strength/', check_password_strength, name='check-password-strength'),
    path('departments/', include(departments_router.urls)),
    path('engagement/', include(engagement_router.urls)),
    path('compensation/', include(compensation_router.urls)),
    path('leave-attendance/', include(leave_attendance_router.urls)),
    path('recruitment/', include(recruitment_router.urls)),

    # Previously unregistered API routers
    path('evaluations/', include(evaluations_router.urls)),
    path('workforce-planning/', include(workforce_router.urls)),
    path('continuous-feedback/', include(feedback_router.urls)),
    path('audit/', include(audit_router.urls)),
    path('dashboard/', include(dashboard_extra_urls)),
    path('dashboard/', include(dashboard_router.urls)),
    path('development-plans/', include(dev_plans_router.urls)),
    path('notifications/', include(notifications_router.urls)),
    path('onboarding/', include(onboarding_router.urls)),
    path('performance-reviews/', include(performance_reviews_router.urls)),
    path('reports/', include(reports_router.urls)),
    path('sentiment/', include(sentiment_router.urls)),
    path('support/', include(support_router.urls)),
    path('wellness/', include(wellness_router.urls)),
    path('search/', search_api_view, name='search-api'),
    

]
