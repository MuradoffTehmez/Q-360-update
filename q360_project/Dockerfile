# ============================================
# Q360 Django Application — Multi-stage Build
# ============================================

# ---- Stage 1: Tailwind CSS Build ----
FROM node:20-alpine AS tailwind-builder

WORKDIR /build

COPY package.json package-lock.json* ./
RUN npm ci --production=false 2>/dev/null || npm install

COPY tailwind.config.js ./
COPY templates/ ./templates/
COPY static_src/ ./static_src/

RUN npx tailwindcss build -o ./tailwind_output.css 2>/dev/null || echo "/* Tailwind build skipped */" > ./tailwind_output.css


# ---- Stage 2: Python Application ----
FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    build-essential \
    libpq-dev \
    redis-tools \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install daphne gunicorn

# Copy project files
COPY . /app/

# Copy Tailwind CSS output from builder stage
COPY --from=tailwind-builder /build/tailwind_output.css /app/static/css/tailwind.css

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media /app/logs

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Make entrypoint executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER appuser

# Expose port
EXPOSE 8000

# Entrypoint handles migrations, collectstatic, etc.
ENTRYPOINT ["/app/entrypoint.sh"]

# Default CMD — gunicorn for HTTP-only mode
# Override to daphne for WebSocket support
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
