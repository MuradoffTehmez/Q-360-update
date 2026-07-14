---
name: debug-fix
description: >
  Q360 layihəsində xəta tapmaq, debug etmək və düzəltmək üçün sistematik yanaşma bələdçisi.
  Django, DRF, Celery, Template, Database, Docker xətalarını kateqoriyalara ayırıb, hər biri
  üçün diaqnostik addımlar və düzəltmə pattern-ləri təqdim edir. Tetikleyicilər: "xəta var",
  "bug", "düzəlt", "fix", "error", "debug", "işləmir", "500 xətası", "404", "template error",
  "import error", "migration error", "IntegrityError", "DoesNotExist", "TemplateDoesNotExist",
  "niyə işləmir", "problem var", "crash", "traceback", "exception".
---

# Debug & Fix — Q360 Xəta Həlli Bələdçisi

Bu skill Q360 layihəsində rast gəlinən xətaları sistematik şəkildə təhlil edib düzəltmək üçün
addım-addım bələdçidir.

## Ümumi Debug Strategiyası

```
1. Xətanı OXUL — traceback-in SON sətirindən başla
2. Xəta TİPİNİ müəyyən et (aşağıdakı kateqoriyalardan)
3. Müvafiq diaqnostik addımları icra et
4. Kök səbəbi tap, təxminlə düzəltmə
5. Düzəltmədən sonra yoxla (manage.py check + test)
```

## Xəta Kateqoriyaları

### 1. Django Model / Migration Xətaları

#### `OperationalError: no such table`
**Səbəb:** Migration tətbiq olunmayıb.
```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
```

#### `ProgrammingError: relation "X" does not exist`
**Səbəb:** PostgreSQL-də tablo yaradılmayıb.
```bash
docker compose exec web python manage.py migrate --run-syncdb
```

#### `IntegrityError: duplicate key` / `UNIQUE constraint failed`
**Səbəb:** Unikal sahəyə dublikat dəyər yazılır.
```python
# Yoxla: unique=True olan sahələri tap
# Fix: get_or_create() istifadə et
obj, created = MyModel.objects.get_or_create(
    unique_field=value,
    defaults={'other_field': 'value'}
)
```

#### `django.db.utils.IntegrityError: null value in column "X"`
**Səbəb:** NOT NULL sahə doldurulmayıb.
```python
# Fix 1: null=True, blank=True əlavə et
field = models.CharField(max_length=100, null=True, blank=True)

# Fix 2: default dəyər ver
field = models.CharField(max_length=100, default='')
```

#### `InconsistentMigrationHistory`
**Səbəb:** Migration faylları ilə DB vəziyyəti uyuşmur.
```bash
# Diaqnostik
docker compose exec web python manage.py showmigrations

# Fix (yalnız dev mühitdə!)
docker compose exec web python manage.py migrate --fake <app> <migration>
```

### 2. Template Xətaları

#### `TemplateDoesNotExist: <template_name>`
**Səbəb:** Template faylı tapılmadı.
```bash
# Yoxla: template faylının yeri düzgündür?
# templates/<app_name>/<template>.html — bu yolda olmalıdır

# settings.py-da TEMPLATES konfiqurasiyasını yoxla
# APP_DIRS: True olmalıdır
```

#### `TemplateSyntaxError`
**Səbəb:** Template-də sintaksis xətası.
```
# Ən çox rast gəlinən:
- {% endblock %} unudulub
- {% load %} tag-i template-in əvvəlində deyil
- Dəyişən adında typo: {{ usre.name }} əvəzinə {{ user.name }}
- Filter xətası: {{ value|dat }} əvəzinə {{ value|date }}
```

#### `NoReverseMatch: Reverse for 'X' not found`
**Səbəb:** URL name-i mövcud deyil və ya argument uyuşmur.
```python
# Yoxla 1: URL name-i düzgün yazılıb?
# urls.py-da name='...' ilə müqayisə et

# Yoxla 2: namespace düzgündür?
# {% url 'evaluations:campaign-list' %} — namespace:name

# Yoxla 3: URL argument uyğundur?
# {% url 'evaluations:campaign-detail' pk=campaign.pk %}
```

### 3. DRF / API Xətaları

#### `401 Unauthorized`
```bash
# Token alıb istifadə et
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "pass"}'

# Token ilə istək göndər
curl -H "Authorization: Bearer <access_token>" \
  http://localhost:8000/api/v1/my-module/
```

#### `403 Forbidden`
**Səbəb:** İstifadəçinin bu əməliyyata icazəsi yoxdur.
```python
# Permission class-ını yoxla
class MyViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    # IsAdminUser, IsAuthenticatedOrReadOnly, DjangoObjectPermissions
```

#### `400 Bad Request — Validation Error`
**Səbəb:** Serializer validation-dan keçməyib.
```python
# Serializer-ə debug əlavə et
serializer = MySerializer(data=request.data)
if not serializer.is_valid():
    print(serializer.errors)  # Xəta detallarını gör
```

#### `405 Method Not Allowed`
**Səbəb:** View bu HTTP method-u dəstəkləmir.
```python
# ViewSet-ə lazım olan action-ları yoxla
# ModelViewSet: GET, POST, PUT, PATCH, DELETE
# ReadOnlyModelViewSet: yalnız GET
```

### 4. Celery Xətaları

#### Task icra olunmur
```bash
# Celery worker işləyir?
docker compose ps celery

# Worker-i restart et
docker compose restart celery

# Redis bağlantısını yoxla
docker compose exec redis redis-cli ping

# Celery loglarını oxu
docker compose logs --tail=100 celery
```

#### `ConnectionError: Error connecting to Redis`
```bash
# Redis konteyneri işləyir?
docker compose ps redis

# Redis restart
docker compose restart redis
```

### 5. Import Xətaları

#### `ImportError: cannot import name 'X' from 'Y'`
```python
# Circular import? → import-u function daxilinə köçür
def my_view(request):
    from apps.other_app.models import OtherModel  # Lazy import
```

#### `ModuleNotFoundError: No module named 'X'`
```bash
# Paket qurulub?
docker compose exec web pip list | grep <package>

# Paket quraşdır və requirements.txt-ə əlavə et
docker compose exec web pip install <package>
echo "<package>==<version>" >> requirements.txt
docker compose up -d --build  # Image rebuild lazımdır
```

### 6. Static Files / CSS-JS Xətaları

#### Static fayllar yüklənmir (404)
```bash
# Collectstatic icra et
docker compose exec web python manage.py collectstatic --noinput

# Nginx static location-ı yoxla
# nginx/nginx.conf-da /static/ location düzgün mapping olmalıdır
```

#### Tailwind class-ları işləmir
```bash
# Tailwind rebuild et
docker compose exec web npx tailwindcss -i ./static_src/input.css \
  -o ./static/css/output.css

# tailwind.config.js-da content path-leri yoxla
# './templates/**/*.html' daxil olmalıdır
```

### 7. Performance Problemləri

#### Yavaş səhifə yükləmə
```bash
# Query sayını yoxla
docker compose exec web python show_dup_queries.py /slow-page/

# Django Debug Toolbar (development)
# settings.py-da INSTALLED_APPS-a 'debug_toolbar' əlavə et
```

#### Memory leak (konteyner OOM)
```bash
# Container resource usage
docker stats

# Celery worker-ə memory limit qoy
# docker-compose.yml:
#   deploy:
#     resources:
#       limits:
#         memory: 512M
```

## Debug Checklist (Hər Xətadan Sonra)

- [ ] Traceback-i tam oxudum
- [ ] Xəta tipini müəyyən etdim
- [ ] Kök səbəbi tapdım (təxmin deyil)
- [ ] Düzəltmə tətbiq etdim
- [ ] `manage.py check` xətasız keçdi
- [ ] Əlaqəli testlər keçdi
- [ ] Düzəltmə başqa yeri pozmadı

## Faydalı Debug Alətləri

```bash
# Django shell-dən model yoxlaması
docker compose exec web python manage.py shell
>>> from apps.my_app.models import MyModel
>>> MyModel.objects.count()
>>> MyModel.objects.filter(status='active').query  # SQL-i gör

# URL-ləri gör
docker compose exec web python manage.py show_urls

# Settings-i yoxla
docker compose exec web python -c "from django.conf import settings; print(settings.DATABASES)"
```
