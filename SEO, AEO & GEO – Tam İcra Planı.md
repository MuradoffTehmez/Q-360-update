# Texniki SEO, AEO & GEO – Tam İcra Planı

Q360 Django/DRF platforması üçün texniki SEO, AEO (Answer Engine Optimization) və GEO (Generative Engine Optimization) ayarlarının tam icra planı.

> [!IMPORTANT]
> Bütün URL-lər nisbi (relative) olacaq. Domen adı `SITE_DOMAIN` env variable vasitəsilə `settings.py`-da saxlanacaq, heç bir yerdə hardcode edilməyəcək.

---

## Proposed Changes

### 1. Settings & Environment Configuration

#### [MODIFY] [settings.py](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/config/settings.py)
- `SITE_DOMAIN` env variable əlavə et (default: `localhost:8000`)
- `SITE_PROTOCOL` env variable əlavə et (default: `https`)
- `SITE_NAME` constant əlavə et (`Q360`)
- `django.contrib.sitemaps` `INSTALLED_APPS`-a əlavə et
- HTTPS/HSTS ayarları: `SECURE_HSTS_SECONDS`, `SECURE_HSTS_INCLUDE_SUBDOMAINS`, `SECURE_HSTS_PRELOAD` (yalnız production-da)
- `seo_context` adlı custom context processor əlavə et
- `'django.contrib.sitemaps'` installed apps-a əlavə et

#### [MODIFY] [.env](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/.env)
- `SITE_DOMAIN=localhost:8000` əlavə et
- `SITE_PROTOCOL=https` əlavə et

#### [MODIFY] [.env.example](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/.env.example)
- Eyni dəyişənləri nümunə olaraq əlavə et

---

### 2. SEO Context Processor

#### [NEW] [seo.py](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/config/seo.py)
- `seo_context(request)` context processor yaradılacaq
- `SITE_DOMAIN`, `SITE_PROTOCOL`, `SITE_NAME`, `SITE_URL` dəyişənlərini bütün template-lərə ötürəcək
- `og:image` üçün tam URL yaradacaq (`{{ SITE_URL }}/static/images/favicon.svg`)

---

### 3. robots.txt (Django View)

#### [MODIFY] [robots.txt](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/templates/robots.txt)
Tam yenidən yazılacaq — bütün autentifikasiya tələb edən route-lar `Disallow`, yalnız açıq səhifələr `Allow`, sitemap ünvanı göstəriləcək:
```
User-agent: *
Allow: /
Allow: /privacy/
Allow: /terms/
Allow: /help/
Disallow: /admin/
Disallow: /api/
Disallow: /accounts/
Disallow: /dashboard/
Disallow: /evaluations/
Disallow: /departments/
Disallow: /reports/
Disallow: /notifications/
Disallow: /pfile/
Disallow: /compensation/
Disallow: /leave/
...bütün auth-tələb edən route-lar
Sitemap: {{ SITE_URL }}/sitemap.xml
```

---

### 4. XML Sitemap

#### [NEW] [sitemaps.py](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/config/sitemaps.py)
- `django.contrib.sitemaps.Sitemap` istifadə edərək `StaticViewSitemap` class yaradılacaq
- Yalnız public səhifələr daxil ediləcək: `/` (home), `/privacy/`, `/terms/`, `/help/`, `/haqqimizda/`, `/faq/`
- `lastmod`, `changefreq`, `priority` doldurulacaq

#### [MODIFY] [urls.py](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/config/urls.py)
- `robots.txt` mövcud TemplateView yerinə Django view ilə əvəz olunacaq (SITE_URL-i sitemap-a inject etmək üçün)
- `/sitemap.xml` route əlavə ediləcək
- `/haqqimizda/` (About) route əlavə ediləcək
- `/faq/` route əlavə ediləcək
- `/llms.txt` route əlavə ediləcək

---

### 5. base.html Yenidən Qurulması (Meta-Tag Sistemi)

#### [MODIFY] [base.html](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/templates/base/base.html)
Mövcud SEO/GEO/AEO bloku tamamilə yenidən yazılacaq:
- `{% block meta_robots %}index, follow{% endblock %}` — daxili səhifələrdə override edib `noindex, nofollow` qoymaq üçün
- `{% block meta_description %}` — mövcud, saxlanacaq amma default Azərbaycan dilində olacaq
- `{% block meta_keywords %}` — block olaraq override edilə bilən
- `{% block og_title %}`, `{% block og_description %}`, `{% block og_image %}` — override edilə bilən OG blokları
- Canonical URL: `{% block canonical_url %}{{ SITE_URL }}{{ request.path }}{% endblock %}`
- hreflang: `SITE_URL` istifadə edəcək (hardcode yox)
- **Bütün JSON-LD blokları `{% block structured_data %}` ilə əhatə ediləcək** ki, child template-lər öz schema-larını əlavə edə bilsin
- Organization + WebSite JSON-LD (global, bütün səhifələrdə)
- SoftwareApplication JSON-LD (global)
- BreadcrumbList JSON-LD (`{% block breadcrumb_schema %}`)

---

### 6. Structured Data (JSON-LD)

**base.html-ə əlavə olunanlar (global):**
- `Organization` schema: ad, url, logo, contactPoint
- `WebSite` schema: ad, url, potentialAction (SearchAction)
- `SoftwareApplication` schema (mövcud, genişləndiriləcək)

**landing.html-ə əlavə olunanlar:**
- `FAQPage` schema (FAQ bölməsi ilə birlikdə)

**Hər səhifədə (base.html-dən):**
- `BreadcrumbList` schema (mövcud breadcrumb sistemindən istifadə edərək)

---

### 7. AEO - Açıq Səhifələrdə Sual-Cavab Formatı

#### [MODIFY] [landing.html](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/templates/landing.html)
- "Q360 nədir?" — 40-60 sözlük birbaşa cavab + detallandırma
- "Q360 hansı HR proseslərini avtomatlaşdırır?" — siyahı formatında
- "Competency Framework nədir?" — aydın tərif
- "Performance Reviews necə işləyir?" — addım-addım
- "9-Box Grid nədir?" — tərif + cədvəl
- "Succession Planning nədir?" — tərif
- FAQ bölməsi (accordion) + FAQPage JSON-LD

#### [NEW] [haqqimizda.html](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/templates/base/haqqimizda.html)
- Aydın "Haqqımızda" bölməsi: kim, nə vaxt, missiya
- ContactPoint schema ilə

#### [NEW] [faq.html](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/templates/base/faq.html)
- Ayrıca FAQ səhifəsi, landing-dəki FAQ-la sinxronlaşdırılmış
- FAQPage JSON-LD

---

### 8. GEO - Generative Engine Optimization

#### [NEW] [llms.txt](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/templates/llms.txt)
AI modellərinə Q360-un nə olduğunu qısa formatda təqdim edən fayl:
```
# Q360
## Platform Description
Q360 is a Django/DRF-based 360° HR/ERP platform...
## Key Features
- Competency Framework
- Performance Reviews
...
## Site Structure
/ — Landing page
/haqqimizda/ — About
/faq/ — FAQ
...
```

---

### 9. Mövcud Səhifələrə noindex/nofollow

Autentifikasiya tələb edən bütün template-lərdə əlavə blok:
```django
{% block meta_robots %}noindex, nofollow{% endblock %}
```

Bu, `base.html`-dəki default `index, follow`-u override edəcək. Mövcud template-lərin hər birini yoxlayıb əlavə edəcəyəm (dashboard, evaluations, reports, departments, və s.)

---

## Verification Plan

### Automated Tests
- `python manage.py check` — template/settings xətaları yoxlanacaq
- `/sitemap.xml` endpoint-inin 200 qaytardığını yoxlayacağıq
- `/robots.txt` endpoint-inin düzgün `Disallow` qaydalarını göstərdiyini yoxlayacağıq

### Manual Verification
- Landing page-in HTML source-unda JSON-LD bloklarının mövcudluğunu yoxlayacağıq
- `robots.txt`-in `Sitemap:` sətirini yoxlayacağıq
- Meta tag-ların hər blokda override edildiyini yoxlayacağıq
