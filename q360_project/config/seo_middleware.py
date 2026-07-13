"""
SEO Middleware
──────────────
Automatically injects noindex/nofollow meta-directive via an HTTP header
for any page that requires authentication. This is a defense-in-depth
measure complementing robots.txt Disallow rules.

Public pages (landing, about, faq, privacy, terms, help) are explicitly
whitelisted and receive the default indexable behavior.
"""


# Paths that ARE public and should be indexed.
# Everything else is treated as private / authenticated.
PUBLIC_PATHS = frozenset({
    '/',
    '/haqqimizda/',
    '/faq/',
    '/privacy/',
    '/terms/',
    '/help/',
    '/robots.txt',
    '/sitemap.xml',
    '/llms.txt',
})


class SEORobotsMiddleware:
    """
    Sets ``X-Robots-Tag: noindex, nofollow`` header on every response whose
    path is NOT in the public whitelist.  Search engine crawlers that honour
    this header will skip indexing even if they somehow bypass robots.txt.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        path = request.path

        # Static / media assets should not carry the header
        if path.startswith(('/static/', '/media/')):
            return response

        if path not in PUBLIC_PATHS:
            response['X-Robots-Tag'] = 'noindex, nofollow'

        return response
