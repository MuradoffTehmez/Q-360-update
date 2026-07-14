---
name: q360-konvensiya
description: >
  Q360 layihəsinin kod konvensiyalarını, arxitektura qaydalarını və texniki standartlarını bilən əsas
  referans skill. Bu skill hər hansı bir kod dəyişikliyi, yeni modul yaratma, refaktorinq və ya
  debug zamanı avtomatik tetiklənməlidir. "Konvensiyaya uyğun yaz", "layihə qaydalarına bax",
  "standarta uyğunlaşdır", "bu doğru yazılıb?", "code review et" kimi istəklərdə devreye gir.
  Həmçinin digər skill-lər (django-modul-yarat, api-endpoint-yarat və s.) bu skill-in qaydalarına
  istinad etməlidir.
---

# Q360 Layihə Konvensiyaları

Bu skill Q360 platformasının (Django 5.1 + DRF + Tailwind + PostgreSQL + Celery + Redis) tam
konvensiya məlumat bazasıdır. İstənilən kod yazanda, review edəndə və ya debug edəndə bu
qaydalara əməl et.

## Texnoloji Yığma (Tech Stack)

| Komponent | Texnologiya | Versiya |
|-----------|-------------|---------|
| Backend Framework | Django | 5.1+ |
| REST API | Django REST Framework | 3.15+ |
| API Docs | drf-spectacular (Swagger/Redoc) | 0.27+ |
| Auth | JWT (SimpleJWT) | 5.4+ |
| Database | PostgreSQL | 16 |
| Cache & Broker | Redis | 7 |
| Async Tasks | Celery + django-celery-beat | 5.4+ |
| WebSocket | Django Channels + Daphne | 4.1+ |
| CSS Framework | TailwindCSS | 3.x |
| Audit Trail | django-simple-history | 3.8+ |
| Admin | django-unfold | 0.42+ |
| Error Tracking | Sentry SDK | 2.19+ |
| MFA | pyotp + qrcode | - |
| WSGI/ASGI Server | Daphne (ASGI) | 4.1+ |
| Reverse Proxy | Nginx | Alpine |
| Containerization | Docker + Docker Compose | - |

## Layihə Strukturu

```
q360_project/
├── config/               # Django settings, urls, celery, seo, sitemaps
│   ├── settings.py       # Əsas parametrlər
│   ├── urls.py           # Root URL routing
│   ├── api_urls.py       # API v1 URL routing
│   ├── celery.py         # Celery konfiqurasiyası
│   ├── seo.py            # SEO helper
│   └── sitemaps.py       # Sitemap generator
├── apps/                 # Django tətbiqləri (30+ modul)
│   ├── core/             # TimeStampedModel, SoftDeletableModel
│   ├── accounts/         # İstifadəçi idarəetməsi + P-File
│   ├── evaluations/      # 360° qiymətləndirmə (əsas modul)
│   ├── departments/      # Təşkilat strukturu
│   ├── ...               # Digər modullar
│   └── __init__.py
├── templates/            # Jinja2/Django templates
│   ├── base/             # base.html, sidebar.html, navbar.html, footer.html
│   ├── components/       # Yenidən istifadə olunan UI komponentlər
│   └── <app_name>/       # Hər app üçün ayrı template qovluğu
├── static/               # JS, CSS, images
├── media/                # İstifadəçi yükləmələri
├── locale/               # i18n tercümə faylları
├── fixtures/             # Test data
├── docker-compose.yml    # Docker servislər (web, db, redis, celery, nginx, ngrok)
└── manage.py
```

## Model Konvensiyaları

### Base Model

Bütün yeni modellər `apps.core.models.TimeStampedModel`-dən miras almalıdır:

```python
from apps.core.models import TimeStampedModel, SoftDeletableModel

class MyModel(TimeStampedModel):
    # created_at, updated_at avtomatik əlavə olunur
    ...
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Model Adı')
        verbose_name_plural = _('Model Adları')
```

### Standart Sahələr

- `created_at` — `auto_now_add=True` (TimeStampedModel-dən gəlir)
- `updated_at` — `auto_now=True` (TimeStampedModel-dən gəlir)
- `created_by` — `ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)`
- `is_active` — `BooleanField(default=True)` (lazım olduqda)
- `is_deleted` / `deleted_at` — SoftDeletableModel-dən (lazım olduqda)

### verbose_name-lər Azərbaycan dilində yazılmalıdır

```python
title = models.CharField(max_length=200, verbose_name=_('Başlıq'))
```

### Audit Trail

Vacib modellərə `simple_history` əlavə et:

```python
from simple_history.models import HistoricalRecords

class ImportantModel(TimeStampedModel):
    history = HistoricalRecords()
```

### Status Choices

Status sahələri model daxilində `STATUS_CHOICES` kimi təyin olunmalıdır:

```python
STATUS_CHOICES = [
    ('draft', _('Qaralama')),
    ('active', _('Aktiv')),
    ('completed', _('Tamamlanmış')),
    ('archived', _('Arxivlənmiş')),
]
status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
```

## View Konvensiyaları

### Template-based Views

- Fayl adı: `template_views.py` (API views-dan ayrı)
- Class-based views istifadə et: `ListView`, `DetailView`, `CreateView`, `UpdateView`
- `LoginRequiredMixin` hər view-da məcburidir
- Paginasiya: `paginate_by = 10` (və ya 20)

```python
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class MyListView(LoginRequiredMixin, ListView):
    model = MyModel
    template_name = 'my_app/my_list.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('created_by')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(Q(title__icontains=search))
        return queryset.order_by('-created_at')
```

### N+1 Query Optimizasiyası

- `select_related()` — ForeignKey/OneToOne sahələr üçün
- `prefetch_related()` — ManyToMany/Reverse FK sahələr üçün
- `annotate()` — aggregate hesablamalar üçün (count, avg)

### Permission / RBAC

- `@login_required` decorator (function-based views üçün)
- `LoginRequiredMixin` (class-based views üçün)
- RBAC yoxlaması view daxilində, user.role ilə

## URL Konvensiyaları

### App URLs (urls.py)

```python
from django.urls import path
from . import template_views

app_name = 'my_app'

urlpatterns = [
    path('', template_views.MyListView.as_view(), name='list'),
    path('create/', template_views.MyCreateView.as_view(), name='create'),
    path('<int:pk>/', template_views.MyDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', template_views.MyUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', template_views.my_delete, name='delete'),
]
```

### Root URL-ə qeydiyyat (config/urls.py)

```python
path('my-module/', include('apps.my_app.urls', namespace='my_app')),
```

### API URL-ləri (config/api_urls.py)

DRF router ilə qeydiyyat, `/api/v1/` prefix altında.

## Serializer Konvensiyaları

```python
from rest_framework import serializers

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
```

## Template Konvensiyaları

### Extend & Block Sistemi

Bütün template-lər `base/base.html`-dən extend edir:

```html
{% extends "base/base.html" %}
{% load i18n %}

{% block title %}{% trans "Səhifə Adı" %} - Q360{% endblock %}

{% block content %}
  <!-- Səhifə məzmunu buraya -->
{% endblock %}
```

### Əsas Block-lar

- `{% block title %}` — Səhifə başlığı
- `{% block content %}` — Əsas məzmun sahəsi
- `{% block extra_css %}` — Əlavə CSS
- `{% block extra_js %}` — Əlavə JavaScript

### TailwindCSS Komponent Pattern-ləri

- Kart: `bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6`
- Cədvəl: responsive wrapper ilə `<div class="overflow-x-auto">`
- Düymə: `bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-lg`
- Badge/Tag: `inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium`

### i18n

Bütün static mətnlər `{% trans %}` və ya `{% blocktrans %}` ilə sarılmalıdır.
Model verbose_name-lər `_('...')` ilə gettext_lazy istifadə etməlidir.

## Celery Task Konvensiyaları

```python
from celery import shared_task

@shared_task(bind=True, max_retries=3)
def my_async_task(self, param1, param2):
    try:
        # İş məntiqi
        pass
    except Exception as exc:
        self.retry(exc=exc, countdown=60)
```

## Docker Əməliyyatları

```bash
# Tam rebuild
docker compose up -d --build

# Migration
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# System check
docker compose exec web python manage.py check

# Collectstatic
docker compose exec web python manage.py collectstatic --noinput

# Loglar
docker compose logs -f web
docker compose logs -f celery
```

## Test Konvensiyaları

```python
from django.test import TestCase, Client
from django.urls import reverse

class MyModelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='test', password='test123', role='admin'
        )
        self.client.login(username='test', password='test123')

    def test_list_view_200(self):
        response = self.client.get(reverse('my_app:list'))
        self.assertEqual(response.status_code, 200)
```

## Keyfiyyət Tələbləri (Hər Dəyişiklik üçün)

1. `python manage.py check` — xətasız keçməlidir
2. `python manage.py makemigrations` — yeni migrasiyalar yaradılmalıdır
3. `python manage.py migrate` — uğurla tətbiq olunmalıdır
4. Template-lər 375px / 768px / 1440px-də horizontal scroll olmadan göstərilməlidir
5. Console-da JS xətası olmamalıdır
6. N+1 query problemi olmamalıdır
