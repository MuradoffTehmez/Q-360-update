"""
URL Configuration for Q360 Evaluation System.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import TemplateView, RedirectView
from django.views.i18n import set_language
from django.http import JsonResponse
from django.contrib.sitemaps.views import sitemap
from config.sitemaps import sitemaps
from django.db import connection
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.throttling import AnonRateThrottle
from apps.accounts.template_views import dashboard_view
from apps.notifications.template_views import get_recent_notifications
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        "success": True,
        "message": "Q360 API",
        "versions": {"v1": request.build_absolute_uri('/api/v1/')},
        "documentation": request.build_absolute_uri('/api/schema/swagger-ui/')
    })


# ============================================
# Health / Readiness / Liveness Endpoints
# ============================================
def health_check(request):
    """Basic health check — returns 200 if Django is running."""
    return JsonResponse({'status': 'ok', 'service': 'q360'})


def readiness_check(request):
    """Readiness probe — verifies DB and Redis connectivity."""
    checks = {}
    status_code = 200

    # Check database
    try:
        connection.ensure_connection()
        checks['database'] = 'ok'
    except Exception as e:
        checks['database'] = f'error: {str(e)}'
        status_code = 503

    # Check Redis
    try:
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection("default")
        redis_conn.ping()
        checks['redis'] = 'ok'
    except Exception as e:
        checks['redis'] = f'error: {str(e)}'
        status_code = 503

    return JsonResponse({'status': 'ok' if status_code == 200 else 'degraded', 'checks': checks}, status=status_code)


def liveness_check(request):
    """Liveness probe — returns 200 if the process is alive."""
    return JsonResponse({'status': 'alive'})



# Custom throttle for login endpoint
class LoginThrottle(AnonRateThrottle):
    """Throttle for login attempts - 5 per minute."""
    rate = '5/min'


# Throttled Token Obtain View
class ThrottledTokenObtainPairView(TokenObtainPairView):
    """Token Obtain view with throttling for brute-force protection."""
    throttle_classes = [LoginThrottle]

urlpatterns = [
    # Health / Readiness / Liveness (no auth required, no rate limiting)
    path('health/', health_check, name='health-check'),
    path('ready/', readiness_check, name='readiness-check'),
    path('live/', liveness_check, name='liveness-check'),

    # Language switcher (must be outside i18n_patterns)
    path('i18n/setlang/', set_language, name='set_language'),

    # Favicon
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.svg', permanent=True)),

    # Admin Panel
    path('admin/', admin.site.urls),

    # Main pages
    path('', TemplateView.as_view(template_name='landing.html'), name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('dashboard/', include(('apps.dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('help/', TemplateView.as_view(template_name='base/help.html'), name='help'),
    path('privacy/', TemplateView.as_view(template_name='base/privacy.html'), name='privacy'),
    path('terms/', TemplateView.as_view(template_name='base/terms.html'), name='terms'),
    path('haqqimizda/', TemplateView.as_view(template_name='base/haqqimizda.html'), name='haqqimizda'),
    path('faq/', TemplateView.as_view(template_name='base/faq.html'), name='faq'),

    # SEO / AEO / GEO endpoints
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('llms.txt', TemplateView.as_view(template_name='llms.txt', content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Authentication
    path('accounts/', include('apps.accounts.urls')),

    # API Authentication
    path('api/auth/token/', ThrottledTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Template-based app URLs (must come FIRST for HTML pages)
    path('evaluations/', include('apps.evaluations.urls', namespace='evaluations')),
    path('departments/', include('apps.departments.urls', namespace='departments')),
    path('reports/', include('apps.reports.urls', namespace='reports')),
    path('development-plans/', include('apps.development_plans.urls', namespace='development-plans')),
    path('notifications/', include('apps.notifications.urls', namespace='notifications')),
    path('competencies/', include(('apps.competencies.urls', 'competencies'), namespace='competencies')),
    path('training/', include(('apps.training.urls', 'training'), namespace='training')),
    path('audit/', include(('apps.audit.urls', 'audit'), namespace='audit')),
    path('search/', include(('apps.search.urls', 'search'), namespace='search')),
    path('onboarding/', include(('apps.onboarding.urls', 'onboarding'), namespace='onboarding')),
    path('workforce-planning/', include(('apps.workforce_planning.urls', 'workforce_planning'), namespace='workforce-planning')),
    path('feedback/', include(('apps.continuous_feedback.urls', 'continuous_feedback'), namespace='feedback')),
    path('performance-reviews/', include('apps.performance_reviews.urls', namespace='performance_reviews')),

    # Phase 1 Core Engines
    path('workflow/', include('apps.workflow_engine.ui_urls', namespace='workflow_engine_ui')),
    path('approval/', include('apps.approval_engine.ui_urls', namespace='approval_engine_ui')),
    path('access-control/', include('apps.access_control.ui_urls', namespace='access_control_ui')),
    path('policy-engine/', include('apps.policy_engine.ui_urls', namespace='policy_engine_ui')),
    path('feature-flags/', include('apps.feature_flags.ui_urls', namespace='feature_flags_ui')),

    # Platform Settings (admin-only pages)
    path('settings/', include('apps.system_settings.urls', namespace='system_settings')),

    # New HRIS Modules
    path('pfile/', include('apps.accounts.urls_pfile', namespace='pfile')),
    path('compensation/', include('apps.compensation.urls', namespace='compensation')),
    path('leave/', include('apps.leave_attendance.urls', namespace='leave_attendance')),
    path('okr/', include('apps.development_plans.urls_okr', namespace='okr')),
    path('recruitment/', include('apps.recruitment.urls', namespace='recruitment')),
    path('sentiment-analysis/', include(('apps.sentiment_analysis.urls', 'sentiment_analysis'), namespace='sentiment_analysis')),
    path('wellness/', include('apps.wellness.urls', namespace='wellness')),
    path('engagement/', include('apps.engagement.urls', namespace='engagement')),
    path('support/', include(('apps.support.urls', 'support'), namespace='support')),

    # Swagger/Redoc UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='api-docs'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API endpoints (all under /api/ prefix)
    path('api/notifications/', get_recent_notifications, name='api-notifications'),
    path('api/v1/', include('config.api_urls')),
    path('api/', api_root, name='api-root'),
    path('api/', include('config.api_urls')), # Backward compatibility for /api/... calls
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler403 = 'config.urls.custom_403'
handler404 = 'config.urls.custom_404'
handler500 = 'config.urls.custom_500'


def custom_403(request, exception):
    from django.shortcuts import render
    return render(request, 'errors/403.html', status=403)


def custom_404(request, exception):
    from django.shortcuts import render
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    from django.shortcuts import render
    return render(request, 'errors/500.html', status=500)
