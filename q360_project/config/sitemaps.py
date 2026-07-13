"""
XML Sitemap Configuration
─────────────────────────
Only public (non-authenticated) pages are included.
All URLs are built relative to SITE_URL from settings.
"""
from datetime import datetime
from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    """Sitemap for static public pages that do not require authentication."""

    changefreq = 'monthly'
    priority = 0.5
    protocol = 'https'

    # (url_name, priority, changefreq)
    _pages = [
        ('home', 1.0, 'weekly'),
        ('haqqimizda', 0.8, 'monthly'),
        ('faq', 0.8, 'monthly'),
        ('privacy', 0.3, 'yearly'),
        ('terms', 0.3, 'yearly'),
        ('help', 0.6, 'monthly'),
    ]

    def items(self):
        return self._pages

    def location(self, item):
        return reverse(item[0])

    def priority(self, item):
        return item[1]

    def changefreq(self, item):
        return item[2]

    def lastmod(self, item):
        # Static pages – return a fixed "last known update" date.
        # Update this when the content actually changes.
        return datetime(2026, 7, 13)


# Registry used by urls.py
sitemaps = {
    'static': StaticViewSitemap,
}
