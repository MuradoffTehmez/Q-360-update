#!/bin/bash
set -e

# ============================================
# Q360 Docker Entrypoint Script
# Handles database readiness, migrations,
# static files, and server startup.
# ============================================

echo "🚀 Q360 Entrypoint Starting..."

# ---- Wait for PostgreSQL ----
echo "⏳ Waiting for PostgreSQL at ${DB_HOST:-db}:${DB_PORT:-5432}..."
until pg_isready -h "${DB_HOST:-db}" -p "${DB_PORT:-5432}" -U "${DB_USER:-postgres}" -q; do
    echo "   PostgreSQL not ready — retrying in 2s..."
    sleep 2
done
echo "✅ PostgreSQL is ready."

# ---- Wait for Redis ----
echo "⏳ Waiting for Redis..."
until redis-cli -h "${REDIS_HOST:-redis}" -p "${REDIS_PORT:-6379}" ping 2>/dev/null | grep -q PONG; do
    echo "   Redis not ready — retrying in 2s..."
    sleep 2
done
echo "✅ Redis is ready."

# ---- Detect if this is the web container ----
# Only the web container should run migrations, collectstatic, and create superuser.
# Celery workers and beat skip these steps.
IS_WEB=false
case "$1" in
    daphne|gunicorn|uvicorn)
        IS_WEB=true
        ;;
esac

if [ "$IS_WEB" = true ]; then
    # ---- Run Migrations ----
    echo "📦 Running database migrations..."
    python manage.py migrate --noinput
    echo "✅ Migrations complete."

    # ---- Collect Static Files ----
    echo "📁 Collecting static files..."
    python manage.py collectstatic --noinput 2>/dev/null || echo "⚠️  collectstatic skipped (non-critical)."
    echo "✅ Static files collected."

    # ---- Create Superuser (if env vars set) ----
    if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "👤 Creating superuser..."
        python manage.py createsuperuser --noinput 2>/dev/null || echo "   Superuser already exists."
        echo "✅ Superuser ready."
    fi

    # ---- Compile Translations ----
    echo "🌐 Compiling translations..."
    python manage.py compilemessages 2>/dev/null || echo "   No translations to compile."
else
    echo "⏭️  Worker mode — skipping migrations/collectstatic."
fi

# ---- Execute CMD ----
echo "🎯 Starting application: $@"
exec "$@"
