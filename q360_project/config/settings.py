"""
Django settings for Q360 Evaluation System.
This is a production-ready settings file for a 360-degree evaluation system
designed for government sector organizations.
"""
import os
from pathlib import Path
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
def env_bool(name: str, default: bool = False) -> bool:
    """
    Convert environment variable values to booleans.
    Recognises typical truthy strings so non-standard casing (e.g. "TRUE")
    continues to work when toggling deployment flags.
    """
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {'true', '1', 'yes', 'on'}
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Security Settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production')
DATA_ENCRYPTION_KEY = os.getenv('DATA_ENCRYPTION_KEY')
DEBUG = env_bool('DEBUG', True)  # Development mode
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'https://*.ngrok-free.dev').split(',')
# ========================================
# SEO / SITE IDENTITY (no hardcoded domains)
# ========================================
SITE_PROTOCOL = os.getenv('SITE_PROTOCOL', 'https')
SITE_DOMAIN = os.getenv('SITE_DOMAIN', 'localhost:8000')
SITE_NAME = 'Q360'
SITE_URL = f'{SITE_PROTOCOL}://{SITE_DOMAIN}'  # computed, never hardcoded
# Content Security Policy (CSP) Configuration
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    "https://cdnjs.cloudflare.com",
    "https://cdn.jsdelivr.net",
    "https://fonts.googleapis.com",
    "https://unpkg.com"
)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    "'unsafe-eval'",
    "https://cdn.tailwindcss.com",
    "https://cdn.jsdelivr.net",
    "https://code.jquery.com",
    "https://cdnjs.cloudflare.com",
    "https://unpkg.com"
)
CSP_FONT_SRC = ("'self'", "https://cdnjs.cloudflare.com", "https://fonts.gstatic.com", "data:")
CSP_IMG_SRC = ("'self'", "data:", "https://images.unsplash.com", "https://ui-avatars.com", "https://*")
CSP_CONNECT_SRC = ("'self'", "ws:", "wss:")
# Application definition
INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',
    'unfold.contrib.import_export',
    'unfold.contrib.guardian',
    'unfold.contrib.simple_history',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',   # XML sitemap for SEO
    'django.contrib.postgres',  # PostgreSQL full-text search
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'simple_history',
    'mptt',  # Django MPTT for hierarchical data
    'channels',  # Real-time notifications / WebSocket
    'csp',  # Content Security Policy
    'django_celery_beat',  # Periodic tasks scheduler
    'drf_spectacular',  # API Documentation
    # 'django_ratelimit',  # Rate limiting (handled by custom middleware)
    # Local apps
    'apps.core',
    'apps.workflow_engine',
    'apps.approval_engine',
    'apps.access_control',
    'apps.policy_engine',
    'apps.feature_flags',
    'apps.accounts',
    'apps.departments',
    'apps.evaluations',
    'apps.performance_reviews',
    'apps.notifications',
    'apps.reports',
    'apps.development_plans',
    'apps.audit',
    'apps.sentiment_analysis',
    'apps.support',
    'apps.competencies',
    'apps.training',
    'apps.search',
    'apps.workforce_planning',
    'apps.continuous_feedback',
    'apps.compensation',
    'apps.leave_attendance',
    'apps.recruitment',
    'apps.dashboard',
    'apps.onboarding',
    'apps.wellness',
    'apps.engagement',
    'apps.system_settings',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files
    'csp.middleware.CSPMiddleware',  # Content Security Policy
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # i18n support
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Two-Factor Authentication Middleware
    'apps.accounts.middleware.two_factor_middleware.TwoFactorAuthMiddleware',
    'apps.accounts.middleware.two_factor_middleware.Session2FAMiddleware',
    # Rate Limiting Middleware
    'apps.accounts.middleware.rate_limit_middleware.RateLimitMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    # Session Tracking (security audit)
    'apps.security.session_tracking.SessionTrackingMiddleware',
    # Custom API Logging
    'config.log_utils.APILoggingMiddleware',
    # SEO: noindex header for authenticated pages
    'config.seo_middleware.SEORobotsMiddleware',
]
ROOT_URLCONF = 'config.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'templates' / 'base',  # expose shared base layout as root-level template
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',  # i18n support
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'config.seo.seo_context',  # SEO/GEO/AEO site identity
            ],
        },
    },
]
WSGI_APPLICATION = 'config.wsgi.application'
# Database
# Use SQLite for development (switch to PostgreSQL for production)
# SQLite Configuration (for development/testing only)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#         'OPTIONS': {
#             'timeout': 20,  # Increase timeout to 20 seconds to avoid database locked errors
#         },
#     }
# }
# PostgreSQL Configuration (ACTIVE)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'q360_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,  # Connection pooling — reuse connections for 10 min
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}
# Custom User Model
AUTH_USER_MODEL = 'accounts.User'
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# Internationalization
LANGUAGE_CODE = 'az'  # Default language: Azerbaijani
LANGUAGES = [
    ('az', _('Azərbaycan')),
    ('en', _('English')),
]
TIME_ZONE = 'Asia/Baku'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# Locale paths
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Whitenoise Configuration for Static File Compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
    'DEFAULT_RENDERER_CLASSES': [
        'apps.core.renderers.StandardizedJSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer',  # Disabled - use template views for HTML
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/min',    # anonim istifadəçilər üçün dəqiqədə 30 sorğu
        # 60/min UI-nin öz API çağırışlarını (bildirişlər + səhifə məlumatları) bloklayıb
        # 429 xətaları yaradırdı — hər səhifə yüklənməsi 2-4 API sorğusu edir
        'user': '300/min',   # autentifikasiyalı istifadəçilər üçün dəqiqədə 300 sorğu
        'login': '5/min',    # 5 login attempts per minute (used for login endpoints)
    },
}
# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}
# CORS Settings
CORS_ALLOWED_ORIGINS = os.getenv(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000'
).split(',')
# Cache Configuration — Redis (used by Django, Celery, and Channels)
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            },
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
        },
        'KEY_PREFIX': 'q360',
        'TIMEOUT': 300,  # 5 minutes default timeout
    }
}
# Celery Broker & Backend — always use Redis (even in dev via Docker)
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', os.getenv('REDIS_URL', 'redis://localhost:6379/0'))
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', os.getenv('REDIS_URL', 'redis://localhost:6379/0'))
# Celery Configuration
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
from celery.schedules import crontab
CELERY_BEAT_SCHEDULE = {
    'update-real-time-statistics-every-5-minutes': {
        'task': 'apps.dashboard.tasks.update_real_time_statistics_task',
        'schedule': crontab(minute='*/5'),
    },
}
# Email Configuration
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@q360.gov.az')
# Professional Logging Configuration
# Multi-level logging with rotation, JSON formatting for production monitoring
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # ========== FORMATTERS ==========
    'formatters': {
        # Verbose format for detailed debugging
        'verbose': {
            'format': '[{levelname}] {asctime} | {name}:{lineno} | {funcName} | {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        # Standard format for general logging
        'standard': {
            'format': '[{levelname}] {asctime} | {module} | {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        # Simple format for console
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
        # JSON format for production monitoring and log aggregation
        'json': {
            'format': '{levelname} {asctime} {name} {funcName} {lineno} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    # ========== FILTERS ==========
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # ========== HANDLERS ==========
    'handlers': {
        # Console handler - for development
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose' if DEBUG else 'standard',
            'filters': ['require_debug_true'] if not DEBUG else [],
        },
        # Main application log - rotating file handler
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'q360.log',
            'maxBytes': 1024 * 1024 * 15,  # 15 MB
            'backupCount': 10,  # Keep 10 backup files
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        # Error log - separate file for errors only
        # Warning log - separate file for warnings
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'warning.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'error.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        # Security log - authentication, permissions, audit
        'security_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 15,  # Keep more security logs
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        # Database log - for query optimization
        'database_file': {
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'database.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        # Performance log - slow requests and performance metrics
        'performance_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'performance.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 7,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        # API log - REST API calls and responses
        'api_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'api.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 7,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # Celery log - background tasks
        'celery_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'celery.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 7,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        # Mail admins on critical errors (production only)
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'verbose',
        },
    },
    # ========== ROOT LOGGER ==========
    'root': {
        'handlers': ['console', 'file', 'error_file', 'warning_file'],
        'level': 'INFO',
    },
    # ========== LOGGERS ==========
    'loggers': {
        # Django core loggers
        'django': {
            'handlers': ['console', 'file', 'error_file', 'warning_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Django request logger - HTTP requests
        'django.request': {
            'handlers': ['file', 'error_file', 'mail_admins'],
            'level': 'WARNING',
            'propagate': False,
        },
        # Django database logger - SQL queries
        'django.db.backends': {
            'handlers': ['database_file'] if DEBUG else [],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': False,
        },
        # Django security logger
        'django.security': {
            'handlers': ['security_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Django server logger
        'django.server': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Custom app loggers
        'apps.accounts': {
            'handlers': ['file', 'security_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.evaluations': {
            'handlers': ['file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.audit': {
            'handlers': ['file', 'security_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps.reports': {
            'handlers': ['file', 'performance_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # REST Framework API logger
        'rest_framework': {
            'handlers': ['api_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Celery task logger
        'celery': {
            'handlers': ['celery_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery.task': {
            'handlers': ['celery_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
# CELERY BEAT SCHEDULE
CELERY_BEAT_SCHEDULE = {
    'send-deadline-reminders-every-day': {
        'task': 'apps.evaluations.tasks.send_deadline_reminders',
        'schedule': 86400.0,  # every 24 hours (or use crontab(hour=9, minute=0))
    },
}
# Content Security Policy settings (Updated for django-csp 4.0+)
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'base-uri': ("'self'",),
        'connect-src': ("'self'", "https://api.example.com"),
        'default-src': ("'self'",),
        'font-src': ("'self'", "https://cdnjs.cloudflare.com"),
        'frame-ancestors': ("'none'",),
        'img-src': ("'self'", "data:", "https:", "https://cdn.tailwindcss.com"),
        'script-src': ("'self'", "'unsafe-inline'", "https://cdn.tailwindcss.com", "https://code.jquery.com", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"),
        'style-src': ("'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com"),
        'upgrade-insecure-requests': True
    }
}
# Rate limiting for authentication endpoints
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['login'] = '5/min'  # Limit login attempts
# Unfold Admin Interface Configuration - Ultra Professional SaaS Look
from django.templatetags.static import static

UNFOLD = {
    "SITE_TITLE": "Q360 Admin",
    "SITE_HEADER": "Q360 - 360° Performance Management",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("images/favicon.svg"),
        "dark": lambda request: static("images/favicon.svg"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("images/favicon.svg"),
        "dark": lambda request: static("images/favicon.svg"),
    },
    "SITE_SYMBOL": "speed",  # Material symbol
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "TABS": [
        {
            "models": [
                "workflow_engine.workflowtemplate",
                "workflow_engine.workflowstep",
                "workflow_engine.workflowcondition",
                "workflow_engine.workflowtransition",
            ],
            "items": [
                {
                    "title": "İş Axını Şablonları",
                    "link": "/admin/workflow_engine/workflowtemplate/",
                    "icon": "account_tree",
                },
                {
                    "title": "Şərtlər",
                    "link": "/admin/workflow_engine/workflowcondition/",
                    "icon": "rule",
                },
            ],
        },
        {
            "models": [
                "approval_engine.approvalchain",
                "approval_engine.approvalrequest",
                "approval_engine.approvaldelegation",
            ],
            "items": [
                {
                    "title": "Təsdiq Zəncirləri",
                    "link": "/admin/approval_engine/approvalchain/",
                    "icon": "verified",
                },
                {
                    "title": "Müraciətlər",
                    "link": "/admin/approval_engine/approvalrequest/",
                    "icon": "pending_actions",
                },
                {
                    "title": "Səlahiyyətlər",
                    "link": "/admin/approval_engine/approvaldelegation/",
                    "icon": "assignment_ind",
                },
            ],
        },
    ],
}
# Django Channels Configuration — WebSocket support via Redis
ASGI_APPLICATION = 'config.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [os.getenv('REDIS_URL', 'redis://localhost:6379/0')],
        },
    },
}
# ========================================
# SENTRY ERROR TRACKING (optional)
# ========================================
SENTRY_DSN = os.getenv('SENTRY_DSN', '')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
            RedisIntegration(),
        ],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment='production' if not DEBUG else 'development',
    )
# ========================================
# TWO-FACTOR AUTHENTICATION (2FA) SETTINGS
# ========================================
# Require 2FA for admin and superadmin roles
TWO_FA_REQUIRED_FOR_ADMINS = env_bool('2FA_REQUIRED_FOR_ADMINS', True)
# 2FA session timeout in minutes (default: 60 minutes)
TWO_FA_SESSION_TIMEOUT = int(os.getenv('2FA_SESSION_TIMEOUT', '60'))
# Company name for 2FA QR codes
COMPANY_NAME = os.getenv('COMPANY_NAME', 'Q360 Evaluation System')
# ========================================
# RATE LIMITING SETTINGS
# ========================================
# Rate limit configurations (requests/window in seconds)
RATELIMIT_ENABLE = env_bool('RATELIMIT_ENABLE', True)
# Login rate limiting: 5 attempts per 5 minutes
LOGIN_RATE_LIMIT = os.getenv('LOGIN_RATE_LIMIT', '5/5m')
# API rate limiting: 60 requests per minute
API_RATE_LIMIT = os.getenv('API_RATE_LIMIT', '60/m')
# General rate limiting: 100 requests per minute
GENERAL_RATE_LIMIT = os.getenv('GENERAL_RATE_LIMIT', '100/m')
# Rate limit view - uses custom error page
RATELIMIT_VIEW = 'apps.accounts.middleware.rate_limit_middleware.ratelimit_handler'
# ========================================
# REST FRAMEWORK & SWAGGER SETTINGS
# ========================================
REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'drf_spectacular.openapi.AutoSchema'
SPECTACULAR_SETTINGS = {
    'TITLE': 'Q360 Evaluation System API',
    'DESCRIPTION': 'API endpoints for Q360 Performance and Development Platform',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    'COMPONENT_SPLIT_REQUEST': True,
}

RATELIMIT_ENABLE = True

# Disable Celery hijacking the root logger so it uses Django's loggers
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

# ========================================
# HTTPS / HSTS SECURITY (production only)
# ========================================
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31536000          # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    
    # Do not redirect Docker healthcheck to HTTPS, otherwise healthcheck fails
    SECURE_REDIRECT_EXEMPT = [r'^health/$']
else:
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
    SECURE_REFERRER_POLICY = 'same-origin'
