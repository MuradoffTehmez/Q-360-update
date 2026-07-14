---
name: celery-task-yarat
description: >
  Q360 layihəsində Celery asinxron tapşırıqlar yaratmaq, planlaşdırmaq və idarə etmək üçün
  bələdçi. E-poçt göndərmə, hesabat yaratma, periodic tasks, retry məntiqi, siqnallarla
  inteqrasiya, task monitoring və django-celery-beat ilə planlaşdırma əhatə edilir.
  Tetikleyicilər: "celery task yarat", "asinxron tapşırıq", "background job", "periodic task",
  "scheduled task", "email göndər", "hesabat yarat", "async task", "queue task", "cron job",
  "beat schedule", "task planning".
---

# Celery Task Yaratma — Q360

Bu skill Q360 layihəsində Celery ilə asinxron tapşırıqlar yaratmaq və idarə etmək üçün
tam bələdçidir.

## Celery Arxitekturası

```
Django Web App → Redis (Broker) → Celery Worker → DB/Email/API
                                  Celery Beat (periodic tasks)
```

- **Broker:** Redis 7 (`redis://redis:6379/0`)
- **Result Backend:** Redis
- **Scheduler:** django-celery-beat (DatabaseScheduler)

## Task Yaratma Pattern-ləri

### 1. Sadə Task

```python
# apps/<module>/tasks.py
import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def simple_task(param1, param2):
    """Sadə asinxron tapşırıq."""
    logger.info(f"Tapşırıq başladı: {param1}, {param2}")
    # İş məntiqi
    result = do_something(param1, param2)
    logger.info(f"Tapşırıq bitdi: {result}")
    return result
```

### 2. Retry ilə Task

```python
@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,  # 60 saniyə
    autoretry_for=(ConnectionError, TimeoutError),
    retry_backoff=True,       # Eksponensial geri çəkilmə
    retry_backoff_max=600,    # Maksimum 10 dəqiqə
    retry_jitter=True,        # Random jitter
)
def reliable_task(self, data_id):
    """Retry məntiqi olan etibarlı tapşırıq."""
    try:
        logger.info(f"Tapşırıq cəhdi #{self.request.retries + 1} — data_id={data_id}")
        result = process_data(data_id)
        return {'success': True, 'data_id': data_id, 'result': result}
    except Exception as exc:
        logger.error(f"Tapşırıq xətası: {exc}", exc_info=True)
        raise self.retry(exc=exc)
```

### 3. E-poçt Göndərmə Task

```python
@shared_task(bind=True, max_retries=3)
def send_notification_email(self, user_id, template_name, context_data):
    """Bildiriş e-poçtu göndər."""
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from apps.accounts.models import User

    try:
        user = User.objects.get(pk=user_id)
        html_message = render_to_string(
            f'emails/{template_name}.html', context_data
        )
        send_mail(
            subject=context_data.get('subject', 'Q360 Bildiriş'),
            message='',
            from_email=None,  # DEFAULT_FROM_EMAIL istifadə edir
            recipient_list=[user.email],
            html_message=html_message,
        )
        logger.info(f"E-poçt göndərildi: {user.email}")
        return {'success': True, 'email': user.email}
    except User.DoesNotExist:
        logger.error(f"User {user_id} tapılmadı")
        return {'success': False, 'error': 'User not found'}
    except Exception as exc:
        logger.error(f"E-poçt xətası: {exc}")
        raise self.retry(exc=exc, countdown=120)
```

### 4. Hesabat Generasiya Task

```python
@shared_task(bind=True, max_retries=2, time_limit=300)
def generate_report(self, report_type, filters, user_id):
    """PDF/Excel hesabat yaradır."""
    from apps.reports.generators import ReportGenerator
    from apps.accounts.models import User

    try:
        user = User.objects.get(pk=user_id)
        generator = ReportGenerator(report_type, filters)

        # Hesabatı yarat
        file_path = generator.generate()

        # İstifadəçiyə bildiriş göndər
        send_notification_email.delay(
            user_id=user_id,
            template_name='report_ready',
            context_data={
                'subject': 'Hesabatınız hazırdır',
                'report_type': report_type,
                'download_url': file_path,
            }
        )

        return {'success': True, 'file_path': file_path}
    except Exception as exc:
        logger.error(f"Hesabat xətası: {exc}")
        raise self.retry(exc=exc)
```

### 5. Toplu Əməliyyat Task (Batch Processing)

```python
@shared_task(bind=True)
def bulk_process(self, item_ids, action):
    """Toplu əməliyyat — böyük siyahını hissələrə ayırır."""
    from apps.my_module.models import MyEntity

    total = len(item_ids)
    processed = 0
    errors = []

    for item_id in item_ids:
        try:
            item = MyEntity.objects.get(pk=item_id)
            if action == 'activate':
                item.status = 'active'
                item.save(update_fields=['status', 'updated_at'])
            elif action == 'archive':
                item.status = 'archived'
                item.save(update_fields=['status', 'updated_at'])
            processed += 1
        except MyEntity.DoesNotExist:
            errors.append(f"ID {item_id} tapılmadı")
        except Exception as e:
            errors.append(f"ID {item_id}: {str(e)}")

        # Progress update (hər 10 elementdə bir)
        if processed % 10 == 0:
            self.update_state(
                state='PROGRESS',
                meta={'current': processed, 'total': total}
            )

    return {
        'total': total,
        'processed': processed,
        'errors': errors,
    }
```

## Task-ı Çağırmaq

### View-dan çağırmaq

```python
# Asinxron çağırış
from .tasks import send_notification_email
send_notification_email.delay(user_id=user.id, template_name='welcome', context_data={...})

# Gecikmə ilə çağırış (5 dəqiqə sonra)
send_notification_email.apply_async(
    args=[user.id, 'reminder', {...}],
    countdown=300,
)

# Konkret tarixdə çağırış
from datetime import datetime, timedelta
send_notification_email.apply_async(
    args=[user.id, 'scheduled', {...}],
    eta=datetime.now() + timedelta(hours=1),
)
```

### Signal-dan çağırmaq

```python
# apps/<module>/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyEntity


@receiver(post_save, sender=MyEntity)
def on_entity_created(sender, instance, created, **kwargs):
    if created:
        from .tasks import send_notification_email
        send_notification_email.delay(
            user_id=instance.created_by_id,
            template_name='entity_created',
            context_data={'title': instance.title}
        )
```

## Periodic Tasks (django-celery-beat)

### Admin Panel-dən

Django Admin → Periodic Tasks → Add bölməsindən vizual olaraq planlaşdırma.

### Kod ilə Planlaşdırma

```python
# config/celery.py
from celery.schedules import crontab

app.conf.beat_schedule = {
    # Hər gün saat 08:00-da xatırlatma göndər
    'send-daily-reminders': {
        'task': 'apps.evaluations.tasks.send_deadline_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
    # Hər həftə bazar ertəsi hesabat yarat
    'weekly-report': {
        'task': 'apps.reports.tasks.generate_weekly_report',
        'schedule': crontab(hour=6, minute=0, day_of_week=1),
    },
    # Hər 5 dəqiqədə cache yenilə
    'refresh-cache': {
        'task': 'apps.dashboard.tasks.refresh_dashboard_cache',
        'schedule': 300.0,  # 5 dəqiqə (saniyə)
    },
}
```

## Task Monitoring

```bash
# Aktiv task-lar
docker compose exec celery celery -A config inspect active

# Gözləyən task-lar
docker compose exec celery celery -A config inspect reserved

# Planlanmış task-lar
docker compose exec celery celery -A config inspect scheduled

# Worker statistikası
docker compose exec celery celery -A config inspect stats
```

## Vacib Qaydalar

1. **Lazy import** — Task daxilində model import et (circular import qarşısı)
2. **Serializable parametrlər** — Task-a yalnız int, str, list, dict göndər (Model instance göndərmə!)
3. **Idempotent** — Eyni task təkrar icra olunsa eyni nəticəni verməlidir
4. **Timeout** — Uzun task-lara `time_limit` qoy
5. **Logging** — Hər task-da `logger` istifadə et
6. **Error handling** — try/except ilə xətaları tut, retry et
