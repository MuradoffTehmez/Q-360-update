# SEO, AEO & GEO — Tam İcra Hesabatı

Q360 platforması üçün texniki SEO, AEO (Answer Engine Optimization) və GEO (Generative Engine Optimization) ayarlarının tam icra hesabatı.

---

## Dəyişdirilən / Yaradılan Fayllar

### Yaradılan Yeni Fayllar (6 fayl)

| Fayl | Təsvir |
|------|--------|
| [config/seo.py](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/config/seo.py) | Custom context processor — `SITE_URL`, `SITE_NAME`, `CANONICAL_URL`, `OG_IMAGE_URL` dəyişənlərini bütün template-lərə ötürür |
| [config/sitemaps.py](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/config/sitemaps.py) | XML sitemap — yalnız public səhifələr (home, about, faq, privacy, terms, help) daxildir, `lastmod`/`changefreq`/`priority` doldurulub |
| [config/seo_middleware.py](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/config/seo_middleware.py) | Middleware — bütün autentifikasiya tələb edən səhifələrə `X-Robots-Tag: noindex, nofollow` HTTP header əlavə edir |
| [templates/base/haqqimizda.html](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/templates/base/haqqimizda.html) | About səhifəsi — missiya, dəyərlər, modullar, əlaqə; `AboutPage` + `Organization` + `BreadcrumbList` JSON-LD |
| [templates/base/faq.html](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/templates/base/faq.html) | FAQ səhifəsi — 8 sual-cavab, accordion UI, `FAQPage` + `BreadcrumbList` JSON-LD |
| [templates/llms.txt](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/templates/llms.txt) | AI/LLM modelləri üçün platform haqqında qısa, maşın-oxuna bilən təsvir |

---

### Dəyişdirilən Mövcud Fayllar (7 fayl)

| Fayl | Dəyişiklik |
|------|------------|
| [config/settings.py](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/config/settings.py) | `SITE_DOMAIN`/`SITE_PROTOCOL`/`SITE_NAME`/`SITE_URL` env vars, `django.contrib.sitemaps` installed apps-a, `seo_context` context processor, `SEORobotsMiddleware`, HSTS/HTTPS security headers |
| [.env](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/.env) | `SITE_DOMAIN`, `SITE_PROTOCOL` dəyişənləri əlavə edildi |
| [.env.example](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/.env.example) | Eyni dəyişənlər nümunə olaraq əlavə edildi |
| [config/urls.py](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/config/urls.py) | `sitemap.xml`, `haqqimizda/`, `faq/`, `llms.txt` route-ları əlavə edildi |
| [templates/robots.txt](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/templates/robots.txt) | Tam yenidən yazıldı — bütün auth route-lar `Disallow`, public `Allow`, `Sitemap:` ünvanı |
| [templates/base/base.html](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/templates/base/base.html) | Meta-tag sistemi tamamilə yenidən quruldu: block-based title/description/robots/canonical/OG/Twitter, hreflang, Organization/WebSite/SoftwareApplication JSON-LD |
| [templates/landing.html](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/templates/landing.html) | SEO meta blokları, AEO sual-cavab bölmələri, FAQ link, `BreadcrumbList` + `FAQPage` JSON-LD |
| [templates/dashboard/home.html](file:///c:/Users/Tahmaz%20Muradov/Desktop/Q-360/q360_project/templates/dashboard/home.html) | `{% block meta_robots %}noindex, nofollow{% endblock %}` əlavə edildi |

---

## Detallı Açıqlama

### 1. Texniki SEO Təməli

- **robots.txt**: Bütün autentifikasiya tələb edən 20+ route `Disallow` edildi, yalnız 7 açıq səhifə `Allow`
- **XML Sitemap**: `django.contrib.sitemaps` ilə `/sitemap.xml` endpoint-i yaradıldı, yalnız public 6 səhifə daxildir
- **Meta-tag sistemi**: `base.html`-də block-based meta sistemi — hər child template `title`, `description`, `robots`, `canonical`, `og:*`, `twitter:*` override edə bilər
- **noindex/nofollow**: `SEORobotsMiddleware` bütün non-public səhifələrə `X-Robots-Tag` header əlavə edir. Əlavə olaraq dashboard template-inə HTML meta da əlavə edildi
- **HSTS**: Production-da (`DEBUG=False`) HSTS 1 il, SSL redirect, secure cookies aktiv olur
- **Canonical URL**: Hər səhifədə `SITE_URL + request.path` ilə dinamik olaraq yaradılır

### 2. Structured Data (JSON-LD)

- **Organization**: ad, url, logo, ünvan (Bakı, AZ), contactPoint (email, dil)
- **WebSite**: SearchAction ilə, çoxdilli
- **SoftwareApplication**: applicationCategory, featureList (13 modul sıralanan), publisher, offers
- **BreadcrumbList**: child template-lərdə override edilə bilən block
- **FAQPage**: landing.html və faq.html-də 8 sual-cavab

### 3. AEO (Answer Engine Optimization)

- Landing page-ə "Q360 nədir?" və "Hansı HR proseslərini avtomatlaşdırır?" sual-cavab kartları əlavə edildi
- FAQ səhifəsində 8 sual-cavab: Competency Framework, 360° qiymətləndirmə, 9-Box Grid, Succession Planning, dil dəstəyi, təhlükəsizlik
- Hər cavab 40-60+ sözlük, birbaşa, özünəyetərli formada
- Siyahı, cədvəl (9-Box Grid) və addım-addım formatlar istifadə edildi

### 4. GEO (Generative Engine Optimization)

- **Haqqımızda** səhifəsi: missiya, dəyərlər, 15 modul siyahısı, əlaqə — `ContactPoint` schema ilə
- **llms.txt**: AI modelləri üçün platform təsviri, modul siyahısı, texnoloji stack, səhifə strukturu
- **hreflang**: `az` və `en` versiyaları, `x-default` — bütün URL-lər `SITE_URL` ilə
- Bütün URL-lər `SITE_DOMAIN` env variable-dan oxunur, heç bir yerdə hardcode yoxdur

---

## Qaydalarla Uyğunluq

| Qayda | Status |
|-------|--------|
| Autentifikasiya tələb edən səhifələr indekslənə bilən deyil | ✅ robots.txt + middleware + meta |
| Mövcud Tailwind/dizayn strukturu pozulmayıb | ✅ Yalnız əlavə edilib |
| Domen adı heç bir yerdə hardcode edilməyib | ✅ `SITE_URL` env-dən |
| `SITE_DOMAIN` env variable istifadə edilir | ✅ settings.py, .env, .env.example |
