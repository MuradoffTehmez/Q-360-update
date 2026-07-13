# Q360 DevOps + System Audit + Full Stack Infrastructure Fix

Complete analysis, repair, and production-readiness audit of the Q360 360° Performance Management System.

---

## 🔍 STEP 1 — Repository Audit Report

### Folder Structure
The project has a clean Django structure under `q360_project/` with 22 Django apps in `apps/`, proper `config/` module, `templates/`, `static/`, `nginx/`, `logs/`, and `locale/` directories.

### 🚨 Critical Issues Found

| # | Category | Issue | Severity |
|---|----------|-------|----------|
| 1 | **Docker** | `docker-compose.yml` references `./nginx/nginx.conf` but nginx config is minimal — missing gzip, WebSocket proxy, security headers | 🔴 HIGH |
| 2 | **Docker** | `web` healthcheck uses `curl` but `curl` is NOT installed in the `python:3.12-slim` image | 🔴 HIGH |
| 3 | **Docker** | No `restart: unless-stopped` on `web` service | 🟡 MEDIUM |
| 4 | **Docker** | `celery` and `celery-beat` use `depends_on` without `condition: service_healthy` | 🟡 MEDIUM |
| 5 | **Docker** | No `docker-compose.override.yml` for dev environment | 🟡 MEDIUM |
| 6 | **Django** | `requirements.txt` specifies `Django>=4.2,<5.0` (root) but project uses `Django==5.1.4` (inner) — **conflict** | 🔴 HIGH |
| 7 | **Django** | `channels` is commented out in `INSTALLED_APPS` but `asgi.py` imports `channels` — **will crash** | 🔴 HIGH |
| 8 | **Django** | `CACHES` uses `LocMemCache` instead of Redis — Celery/Channels won't work properly in Docker | 🔴 HIGH |
| 9 | **Django** | `CHANNEL_LAYERS` is commented out — WebSocket will NOT work | 🔴 HIGH |
| 10 | **Django** | `ASGI_APPLICATION` is commented out — Channels/WebSocket disabled | 🔴 HIGH |
| 11 | **Django** | `sentry-sdk` in root requirements.txt but NOT in project requirements.txt and NOT initialized in settings.py | 🟡 MEDIUM |
| 12 | **Django** | `DEBUG=True` default — dangerous for production | 🟡 MEDIUM |
| 13 | **Django** | `ALLOWED_HOSTS = ['*']` — insecure for production | 🟡 MEDIUM |
| 14 | **Django** | Missing `gunicorn` in root requirements.txt | 🟡 MEDIUM |
| 15 | **Django** | `whitenoise` middleware commented out but `whitenoise` is in requirements | 🟡 MEDIUM |
| 16 | **Django** | No health check endpoint in `urls.py` | 🟡 MEDIUM |
| 17 | **PostgreSQL** | `.env.example` password is `T3hmezSecure@2025`, user confirmed password is `Qazzaq2020.TM` | 🟡 MEDIUM |
| 18 | **PostgreSQL** | No `CONN_MAX_AGE` for connection pooling in dev settings | 🟢 LOW |
| 19 | **Redis** | Redis volume not persisted in docker-compose | 🟡 MEDIUM |
| 20 | **Celery** | `celery-beat` has no `--scheduler django_celery_beat.schedulers:DatabaseScheduler` | 🟡 MEDIUM |
| 21 | **Nginx** | Nginx config missing WebSocket proxy pass for `/ws/` | 🔴 HIGH |
| 22 | **Nginx** | No gzip compression enabled | 🟡 MEDIUM |
| 23 | **Security** | `django-csp` middleware commented out but listed in requirements | 🟡 MEDIUM |
| 24 | **Security** | `django_ratelimit` commented out in INSTALLED_APPS | 🟢 LOW |
| 25 | **.env** | No actual `.env` file exists (only `.env.example`) | 🔴 HIGH |
| 26 | **Production** | `production.py` imports from `.base` which doesn't exist — broken settings split | 🔴 HIGH |
| 27 | **Duplicate** | Two `requirements.txt` files (root and inner) with different content | 🟡 MEDIUM |
| 28 | **Dockerfile** | `collectstatic` runs during build without DB/env — may fail | 🟡 MEDIUM |
| 29 | **Docker** | `.dockerignore` excludes `*.md` — but `locale/` needs `.po` files; also excluding `staticfiles/` causes issues | 🟢 LOW |
| 30 | **Tailwind** | `node_modules/` not in `.dockerignore` explicitly, `package-lock.json` present but no build step in Docker | 🟡 MEDIUM |

---

## Proposed Changes

### Component 1: Docker Infrastructure

#### [MODIFY] [docker-compose.yml](file:///c:/Users/Tahmaz Muradov/Desktop/Q-360/q360_project/docker-compose.yml)
- Fix `web` healthcheck to use `python` instead of `curl`
- Add `restart: unless-stopped` to `web` service
- Add `condition: service_healthy` to celery/celery-beat `depends_on`
- Add `--scheduler django_celery_beat.schedulers:DatabaseScheduler` to celery-beat command
- Add Redis persistent volume
- Add `POSTGRES_INITDB_ARGS` for UTF-8 encoding
- Add network configuration
- Fix nginx volume mount path

#### [MODIFY] [Dockerfile](file:///c:/Users/Tahmaz Muradov/Desktop/Q-360/q360_project/Dockerfile)
- Add `curl` installation for healthcheck OR switch to python-based check
- Add Tailwind CSS build stage (multi-stage build)
- Fix `collectstatic` ordering (after env is available via entrypoint)
- Add `daphne` for ASGI/WebSocket support

#### [NEW] docker-compose.override.yml
- Development overrides with DEBUG=True, volume mounts, port mapping

#### [NEW] entrypoint.sh
- Wait for DB, run migrations, collectstatic, then start server

---

### Component 2: Environment Variables

#### [NEW] [.env](file:///c:/Users/Tahmaz Muradov/Desktop/Q-360/q360_project/.env)
- Create from `.env.example` with user's PostgreSQL password `Qazzaq2020.TM`
- Generate proper SECRET_KEY
- Set all required variables for Docker Compose

#### [MODIFY] [.env.example](file:///c:/Users/Tahmaz Muradov/Desktop/Q-360/q360_project/.env.example)
- Add missing variables: `SENTRY_DSN`, `DJANGO_SUPERUSER_*`, `CELERY_*`, `REDIS_URL`

---

### Component 3: Django Settings

#### [MODIFY] [settings.py](file:///c:/Users/Tahmaz Muradov/Desktop/Q-360/q360_project/config/settings.py)
- Uncomment and enable `channels` in `INSTALLED_APPS`
- Uncomment and enable `csp` in `INSTALLED_APPS`
- Uncomment `whitenoise` middleware
- Enable `CHANNEL_LAYERS` with Redis backend
- Enable `ASGI_APPLICATION`
- Switch `CACHES` to Redis backend
- Add Sentry initialization
- Fix `ALLOWED_HOSTS` to use env variable
- Add `CONN_MAX_AGE` for connection pooling
- Add `django_celery_beat` to `INSTALLED_APPS`

#### [DELETE] [config/settings/production.py](file:///c:/Users/Tahmaz Muradov/Desktop/Q-360/q360_project/config/settings/production.py)
- This file imports from a non-existent `.base` module. The main `settings.py` already handles production/development modes via `DEBUG` flag. Remove this broken file.

---

### Component 4: Django URLs & Health Endpoints

#### [MODIFY] [urls.py](file:///c:/Users/Tahmaz Muradov/Desktop/Q-360/q360_project/config/urls.py)
- Add `/health/` endpoint for Docker healthcheck and monitoring
- Add `/ready/` readiness endpoint
- Add `/live/` liveness endpoint

---

### Component 5: Nginx Configuration

#### [MODIFY] [nginx.conf](file:///c:/Users/Tahmaz Muradov/Desktop/Q-360/q360_project/nginx/nginx.conf)
- Add gzip compression
- Add WebSocket proxy for `/ws/`
- Add security headers (X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy)
- Add rate limiting zones
- Add proper proxy headers (X-Forwarded-Proto, X-Real-IP)
- Increase `client_max_body_size`

---

### Component 6: Celery Configuration

Celery config (`config/celery.py`, `config/__init__.py`) is already correct. The fix is in:
- `docker-compose.yml` — add database scheduler to celery-beat
- `settings.py` — add `django_celery_beat` to `INSTALLED_APPS`

---

### Component 7: Entrypoint & Startup Script

#### [NEW] entrypoint.sh
- Wait for PostgreSQL to be ready
- Run `python manage.py migrate --noinput`
- Run `python manage.py collectstatic --noinput`
- Create superuser if `DJANGO_SUPERUSER_*` env vars are set
- Exec gunicorn/daphne

---

### Component 8: Root-level Cleanup

#### [MODIFY] Root [requirements.txt](file:///c:/Users/Tahmaz Muradov/Desktop/Q-360/requirements.txt)
- This root file has wrong Django version constraint. The real requirements are in `q360_project/requirements.txt`. We should update root to match or redirect to project file.

---

## Open Questions

> [!IMPORTANT]
> **Daphne vs Gunicorn**: The project uses Django Channels for WebSocket. In Docker, should we:
> - **Option A (Recommended)**: Use `daphne` as the ASGI server (supports both HTTP + WebSocket in one process)
> - **Option B**: Keep `gunicorn` for HTTP and add a separate `daphne` service for WebSocket
> 
> I recommend **Option A** for simplicity. If you need higher HTTP throughput, Option B is better.

> [!IMPORTANT]
> **Sentry DSN**: Do you have a Sentry DSN to configure? If not, I'll leave it as optional via env variable.

> [!IMPORTANT]
> **Email Configuration**: The `.env.example` has placeholder email config. Do you have real SMTP credentials to use?

> [!IMPORTANT]
> **Domain**: The nginx configs reference `q360.example.com`. What is your actual production domain? For now I'll use `localhost` for Docker Compose local development.

---

## Verification Plan

### Automated Tests
```bash
# Build and start all containers
docker compose up --build -d

# Check all containers are healthy
docker compose ps

# Verify migrations run
docker compose exec web python manage.py showmigrations

# Test health endpoint
curl http://localhost/health/

# Test admin panel
curl -s -o /dev/null -w "%{http_code}" http://localhost/admin/

# Test static files
curl -s -o /dev/null -w "%{http_code}" http://localhost/static/css/tailwind.css

# Check celery worker
docker compose exec celery celery -A config inspect ping

# Check Redis
docker compose exec redis redis-cli ping
```

### Manual Verification
- Access admin panel at `http://localhost/admin/`
- Login with superuser credentials
- Verify WebSocket connection at browser console
- Check Celery task execution
