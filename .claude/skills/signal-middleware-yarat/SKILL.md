---
name: signal-middleware-yarat
description: >
  Q360 layihəsində Django signal handler, middleware, context processor, template tag və template
  filter yaratmaq üçün bələdçi. Mövcud layihədəki pattern-lərə uyğun şəkildə bu komponentləri
  yaratmağı, qeydiyyat etməyi və test etməyi öyrədir. Tetikleyicilər: "signal yarat",
  "middleware yarat", "context processor", "template tag", "template filter", "custom tag",
  "request middleware", "audit middleware", "permission middleware", "signal handler".
---

# Signal, Middleware və Template Tag Yaratma — Q360

## 1. Django Signals

### Signal Handler Pattern

```python
# apps/<module>/signals.py
"""Signal handlers for <module> app."""
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=MyEntity)
def on_entity_saved(sender, instance, created, **kwargs):
    """Entity yaradıldıqda/yeniləndikdə tetiklənir."""
    # Sonsuz loop qarşısı: update_fields yoxla
    update_fields = kwargs.get('update_fields')
    if update_fields and 'cached_field' in update_fields:
        return

    if created:
        logger.info(f"Yeni entity yaradıldı: {instance.pk}")
        # Bildiriş göndər
        try:
            from .tasks import send_notification_email
            send_notification_email.delay(
                user_id=instance.created_by_id,
                template_name='entity_created',
                context_data={'title': instance.title}
            )
        except Exception:
            pass  # Celery olmasa da xəta verməsin
    else:
        logger.info(f"Entity yeniləndi: {instance.pk}")


@receiver(pre_save, sender=MyEntity)
def on_entity_pre_save(sender, instance, **kwargs):
    """Save-dən əvvəl validasiya və ya hesablama."""
    if instance.pk:
        try:
            old = MyEntity.objects.get(pk=instance.pk)
            if old.status != instance.status:
                instance._status_changed = True
                instance._old_status = old.status
        except MyEntity.DoesNotExist:
            pass
```

### apps.py-da Signal Qeydiyyatı

```python
# apps/<module>/apps.py
class MyModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.my_module'
    verbose_name = _('Modul Adı')

    def ready(self):
        try:
            from . import signals  # noqa: F401
        except ImportError:
            pass
```

### Custom Signal Yaratma

```python
# apps/<module>/signals.py
from django.dispatch import Signal

# Custom signal — status dəyişəndə tetiklənir
entity_status_changed = Signal()  # sender, instance, old_status, new_status

# Signal göndərən:
entity_status_changed.send(
    sender=MyEntity,
    instance=instance,
    old_status='draft',
    new_status='active',
)

# Signal qəbul edən (başqa app-da):
from apps.my_module.signals import entity_status_changed

@receiver(entity_status_changed)
def handle_status_change(sender, instance, old_status, new_status, **kwargs):
    logger.info(f"Status dəyişdi: {old_status} → {new_status}")
```

---

## 2. Django Middleware

### Middleware Pattern

```python
# apps/<module>/middleware.py
"""Custom middleware for <module>."""
import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestTimingMiddleware(MiddlewareMixin):
    """Hər request-in icra müddətini ölçür."""

    def process_request(self, request):
        request._start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time
            response['X-Request-Duration'] = f'{duration:.3f}s'
            if duration > 2.0:  # 2 saniyədən yavaş
                logger.warning(
                    f"Yavaş request: {request.method} {request.path} — {duration:.2f}s"
                )
        return response


class AuditMiddleware(MiddlewareMixin):
    """İstifadəçi hərəkətlərini audit log-a yazır."""

    AUDIT_METHODS = ('POST', 'PUT', 'PATCH', 'DELETE')

    def process_response(self, request, response):
        if (
            request.method in self.AUDIT_METHODS
            and hasattr(request, 'user')
            and request.user.is_authenticated
            and response.status_code < 400
        ):
            from apps.audit.models import AuditLog
            AuditLog.objects.create(
                user=request.user,
                action=request.method,
                path=request.path,
                ip_address=self.get_client_ip(request),
                status_code=response.status_code,
            )
        return response

    @staticmethod
    def get_client_ip(request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded.split(',')[0].strip() if x_forwarded else request.META.get('REMOTE_ADDR')


class RoleBasedAccessMiddleware(MiddlewareMixin):
    """RBAC middleware — rol əsaslı URL qoruma."""

    SUPERUSER_PATHS = ['/admin/', '/system/', '/ai/']

    def process_request(self, request):
        if any(request.path.startswith(p) for p in self.SUPERUSER_PATHS):
            if not request.user.is_authenticated or not request.user.is_superuser:
                from django.http import HttpResponseForbidden
                return HttpResponseForbidden('İcazəniz yoxdur.')
```

### settings.py-da Middleware Qeydiyyatı

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... digər middleware-lər ...

    # Custom middleware — sonda əlavə et
    'apps.my_module.middleware.RequestTimingMiddleware',
    'apps.my_module.middleware.AuditMiddleware',
]
```

---

## 3. Context Processors

```python
# apps/<module>/context_processors.py
"""Template context processors for <module>."""
from django.conf import settings


def site_settings(request):
    """Bütün template-lərdə SITE_NAME, SITE_URL əlçatan edir."""
    return {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL,
        'CANONICAL_URL': f'{settings.SITE_URL}{request.path}',
        'OG_IMAGE_URL': f'{settings.SITE_URL}/static/images/og-image.png',
    }


def user_permissions(request):
    """İstifadəçinin icazələrini template-ə ötürür."""
    if not request.user.is_authenticated:
        return {'user_perms': {}}
    return {
        'user_perms': {
            'is_admin': request.user.is_staff or getattr(request.user, 'role', '') == 'admin',
            'is_manager': getattr(request.user, 'role', '') in ['admin', 'manager'],
            'is_superuser': request.user.is_superuser,
        }
    }


def unread_notifications_count(request):
    """Oxunmamış bildiriş sayını template-ə ötürür."""
    if not request.user.is_authenticated:
        return {'unread_notifications': 0}
    from apps.notifications.models import Notification
    count = Notification.objects.filter(
        recipient=request.user, is_read=False
    ).count()
    return {'unread_notifications': count}
```

### settings.py-da Context Processor Qeydiyyatı

```python
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            # Django defaults
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            # Custom
            'apps.my_module.context_processors.site_settings',
            'apps.my_module.context_processors.user_permissions',
        ],
    },
}]
```

---

## 4. Custom Template Tags & Filters

### Template Tag yaratma

```python
# apps/<module>/templatetags/<module>_tags.py
"""Custom template tags for <module>."""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def status_badge(status):
    """Status badge HTML qaytarır."""
    colors = {
        'active': ('green', 'Aktiv'),
        'draft': ('amber', 'Qaralama'),
        'completed': ('blue', 'Tamamlanmış'),
        'archived': ('gray', 'Arxivlənmiş'),
    }
    color, label = colors.get(status, ('gray', status))
    return mark_safe(
        f'<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs '
        f'font-medium bg-{color}-100 text-{color}-800 dark:bg-{color}-900/30 '
        f'dark:text-{color}-400">{label}</span>'
    )


@register.inclusion_tag('components/pagination.html')
def render_pagination(page_obj, request):
    """Pagination komponentini render edir."""
    return {'page_obj': page_obj, 'request': request}


@register.simple_tag(takes_context=True)
def active_link(context, url_name, css_class='active'):
    """Aktiv naviqasiya linki üçün CSS class qaytarır."""
    request = context['request']
    from django.urls import reverse
    try:
        url = reverse(url_name)
        if request.path.startswith(url):
            return css_class
    except Exception:
        pass
    return ''
```

### Template Filter yaratma

```python
@register.filter
def truncate_smart(value, length=50):
    """Mətni ağıllı şəkildə kəsir — söz ortasından kəsmir."""
    if len(value) <= length:
        return value
    truncated = value[:length].rsplit(' ', 1)[0]
    return f'{truncated}...'


@register.filter
def time_since_short(value):
    """Qısa zaman fərqi: '3 dəq əvvəl', '2 saat əvvəl'."""
    from django.utils import timezone
    diff = timezone.now() - value
    seconds = diff.total_seconds()
    if seconds < 60:
        return 'indicə'
    elif seconds < 3600:
        return f'{int(seconds / 60)} dəq əvvəl'
    elif seconds < 86400:
        return f'{int(seconds / 3600)} saat əvvəl'
    else:
        return f'{int(seconds / 86400)} gün əvvəl'
```

### templatetags __init__.py

```
apps/<module>/templatetags/
├── __init__.py    ← Boş fayl
└── <module>_tags.py
```

### Template-də istifadə

```html
{% load my_module_tags %}

{% status_badge item.status %}
{{ item.title|truncate_smart:30 }}
{{ item.created_at|time_since_short }}
```

---

## 5. Management Commands

```python
# apps/<module>/management/commands/my_command.py
"""Custom management command."""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Komanda təsviri'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Dəyişiklik etmədən göstər')
        parser.add_argument('--limit', type=int, default=100, help='Limit sayı')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        limit = options['limit']

        self.stdout.write(f'Komanda başladı (dry_run={dry_run}, limit={limit})')
        # İş məntiqi
        self.stdout.write(self.style.SUCCESS('Komanda uğurla tamamlandı!'))
```

İstifadə:
```bash
docker compose exec web python manage.py my_command --dry-run --limit 50
```
