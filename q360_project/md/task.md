# Q360 DevOps Audit Fix — Task Tracker

## Component 1: Docker Infrastructure
- [ ] Fix `docker-compose.yml` (healthcheck, restart, depends_on, redis volume, network)
- [ ] Fix `Dockerfile` (multi-stage build, entrypoint, daphne)
- [ ] Create `docker-compose.override.yml`

## Component 2: Environment Variables
- [ ] Create `.env` with real credentials
- [ ] Update `.env.example` with missing variables

## Component 3: Django Settings
- [ ] Enable `channels`, `csp`, `django_celery_beat` in INSTALLED_APPS
- [ ] Enable `whitenoise` middleware
- [ ] Enable `CHANNEL_LAYERS` with Redis
- [ ] Enable `ASGI_APPLICATION`
- [ ] Switch `CACHES` to Redis
- [ ] Add Sentry initialization
- [ ] Fix `ALLOWED_HOSTS`
- [ ] Add `CONN_MAX_AGE`
- [ ] Remove broken `config/settings/production.py`

## Component 4: URLs & Health Endpoints
- [ ] Add `/health/`, `/ready/`, `/live/` endpoints

## Component 5: Nginx Configuration
- [ ] Add gzip, WebSocket proxy, security headers, rate limiting

## Component 6: Entrypoint Script
- [ ] Create `entrypoint.sh` (wait for DB, migrate, collectstatic, start)

## Component 7: Root Cleanup
- [ ] Fix root `requirements.txt`

## Component 8: Verification
- [ ] Docker compose build succeeds
- [ ] All containers start healthy
