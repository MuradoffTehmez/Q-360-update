---
name: docker-ops
description: >
  Q360 layihəsinin Docker əməliyyatları — build, migrate, test, deploy, log analizi, container
  idarəetməsi və troubleshooting üçün əməliyyat bələdçisi. Docker Compose ilə servislerin
  idarə olunması (web, db, redis, celery, celery-beat, nginx, ngrok). Tetikleyicilər: "docker",
  "konteyner", "deploy et", "build et", "migrate et", "migration yarat", "log bax", "restart et",
  "servisi yenidən başlat", "database yedəklə", "collectstatic", "docker compose", "konteyner
  düşüb", "servis işləmir", "health check", "manage.py", "celery", "redis".
---

# Docker Əməliyyatları — Q360

Bu skill Q360 layihəsinin Docker Compose mühitində idarə olunması üçün tam əməliyyat bələdçisidir.

## Servis Arxitekturası

```
┌──────────────────────────────────────────────────────┐
│                    Nginx (:80/:443)                    │
│                    Reverse Proxy                       │
└──────────────┬───────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────┐
│              Web (Daphne ASGI) :8000                  │
│              Django 5.1 + Channels                    │
└──────┬────────────┬──────────────┬───────────────────┘
       │            │              │
┌──────▼──────┐ ┌───▼────┐ ┌──────▼──────┐
│ PostgreSQL  │ │ Redis  │ │   Celery    │
│ :5432       │ │ :6379  │ │   Worker    │
│ (postgres:  │ │(redis: │ │ + Beat      │
│  16-alpine) │ │7-alpine│ │             │
└─────────────┘ └────────┘ └─────────────┘
```

## Əsas Docker Compose Komandaları

### Build & Start

```bash
# Tam rebuild (dəyişiklikdən sonra)
docker compose up -d --build

# Sadəcə start (dəyişiklik yoxdursa)
docker compose up -d

# Yalnız web servisini rebuild et
docker compose up -d --build web

# Bütün servisləri dayandır
docker compose down

# Bütün servisləri + volume-ları sil (DİQQƏT: DATA İTKİSİ!)
docker compose down -v
```

### Migration

```bash
# Migration yaratma (yeni model/dəyişiklik sonrası)
docker compose exec web python manage.py makemigrations

# Spesifik app üçün migration
docker compose exec web python manage.py makemigrations my_app

# Migrationları tətbiq et
docker compose exec web python manage.py migrate

# Migration statusunu yoxla
docker compose exec web python manage.py showmigrations

# Migration geri alma
docker compose exec web python manage.py migrate my_app 0001_initial
```

### System Check

```bash
# Django system check (xətasız keçməlidir)
docker compose exec web python manage.py check

# Deployment check
docker compose exec web python manage.py check --deploy

# Spesifik tag ilə check
docker compose exec web python manage.py check --tag models
```

### Static Files

```bash
# Static faylları yığ
docker compose exec web python manage.py collectstatic --noinput

# Tailwind build (development)
docker compose exec web npx tailwindcss -i ./static_src/input.css -o ./static/css/output.css --watch

# Tailwind production build
docker compose exec web npx tailwindcss -i ./static_src/input.css -o ./static/css/output.css --minify
```

### Loglar

```bash
# Bütün servislerin logları
docker compose logs -f

# Yalnız web logları
docker compose logs -f web

# Yalnız celery logları
docker compose logs -f celery

# Son 100 sətir
docker compose logs --tail=100 web

# Xəta axtarışı
docker compose logs web 2>&1 | grep -i error
docker compose logs web 2>&1 | grep -i traceback
```

### Database Əməliyyatları

```bash
# Django shell
docker compose exec web python manage.py shell

# Database shell (psql)
docker compose exec db psql -U postgres -d q360_db

# Database dump (yedəkləmə)
docker compose exec db pg_dump -U postgres q360_db > backup_$(date +%Y%m%d).sql

# Database restore
docker compose exec -T db psql -U postgres q360_db < backup.sql

# Superuser yaratma
docker compose exec web python manage.py createsuperuser
```

### Redis Əməliyyatları

```bash
# Redis CLI
docker compose exec redis redis-cli

# Cache təmizləmə
docker compose exec redis redis-cli FLUSHDB

# Redis status
docker compose exec redis redis-cli INFO
```

### Celery Əməliyyatları

```bash
# Celery worker logları
docker compose logs -f celery

# Celery beat logları
docker compose logs -f celery-beat

# Aktiv task-ları gör
docker compose exec celery celery -A config inspect active

# Planlanmış task-ları gör
docker compose exec celery celery -A config inspect scheduled

# Celery worker restart
docker compose restart celery celery-beat
```

### Test Əməliyyatları

```bash
# Bütün testlər
docker compose exec web python manage.py test

# Spesifik app testi
docker compose exec web python manage.py test apps.evaluations

# Smoke test — bütün səhifələr 200 qaytarır?
docker compose exec web python smoke_new_pages.py

# N+1 query yoxlaması
docker compose exec web python show_dup_queries.py /page-url/

# Coverage report
docker compose exec web coverage run manage.py test
docker compose exec web coverage report
```

### i18n (Tercümə)

```bash
# Mesajları çıxar
docker compose exec web python manage.py makemessages -l az

# Mesajları compile et
docker compose exec web python manage.py compilemessages
```

## Troubleshooting

### Konteyner düşür / restart loop

```bash
# Status yoxla
docker compose ps

# Exit code-a bax
docker compose ps -a

# Konteyner loglarını oxu
docker compose logs --tail=50 <service_name>
```

### Database connection error

```bash
# DB konteynerin sağlamlığını yoxla
docker compose exec db pg_isready -U postgres

# DB konteyneri restart et
docker compose restart db

# 30 saniyə gözlə, sonra web restart
docker compose restart web
```

### Port conflict

```bash
# Portları yoxla
netstat -ano | findstr :8000
netstat -ano | findstr :5432
netstat -ano | findstr :6379

# Conflict olan prosesi öldür
taskkill /PID <pid> /F
```

### Memory / Disk full

```bash
# Docker disk usage
docker system df

# Unused resources təmizlə
docker system prune -af

# Dangling volumes sil
docker volume prune
```

## Health Check URL-ləri

| Endpoint | Məqsəd | Gözlənilən |
|----------|--------|------------|
| `/health/` | Əsas sağlamlıq yoxlaması | `{"status": "ok"}` |
| `/ready/` | Readiness (DB + Redis) | `{"status": "ok", "checks": {...}}` |
| `/live/` | Liveness probe | `{"status": "alive"}` |

## Environment Variables (.env)

Mühit dəyişənləri `.env` faylında saxlanır. Nümunə üçün `.env.example`-a bax.
Heç vaxt `.env` faylını git-ə commit etmə (`.gitignore`-da olmalıdır).

Əsas dəyişənlər:
- `SECRET_KEY` — Django secret key
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `REDIS_URL` — Redis connection string
- `ALLOWED_HOSTS` — İcazə verilən host-lar
- `DEBUG` — Debug mode (production-da `False`)
- `NGROK_AUTHTOKEN` — Ngrok tunnel üçün
- `SENTRY_DSN` — Sentry error tracking
