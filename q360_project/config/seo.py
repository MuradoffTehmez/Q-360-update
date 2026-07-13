"""
SEO / GEO / AEO Context Processor
──────────────────────────────────
Injects site identity variables into every template context so that
meta tags, canonical URLs, Open Graph tags and JSON-LD schemas can be
built without any hardcoded domain names.

All values are sourced from settings which in turn read from environment
variables, making the SEO layer fully configurable per deployment.
"""
from django.conf import settings


def seo_context(request):
    """
    Makes SEO-related constants available to every template.

    Template variables provided
    ───────────────────────────
    SITE_NAME        – "Q360"
    SITE_DOMAIN      – e.g. "q360.az" (from env)
    SITE_PROTOCOL    – "https" or "http" (from env)
    SITE_URL         – e.g. "https://q360.az" (computed)
    CANONICAL_URL    – full canonical for the current page
    OG_IMAGE_URL     – absolute URL to the default sharing image
    """
    site_url = getattr(settings, 'SITE_URL', '')
    canonical = f"{site_url}{request.path}"

    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Q360'),
        'SITE_DOMAIN': getattr(settings, 'SITE_DOMAIN', ''),
        'SITE_PROTOCOL': getattr(settings, 'SITE_PROTOCOL', 'https'),
        'SITE_URL': site_url,
        'CANONICAL_URL': canonical,
        'OG_IMAGE_URL': f"{site_url}/static/images/favicon.svg",
    }
