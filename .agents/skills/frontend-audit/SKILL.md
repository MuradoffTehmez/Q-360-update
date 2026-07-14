---
name: frontend-audit
description: >
  Q360 layihəsinin frontend keyfiyyət auditi — mobil responsive yoxlama, Tailwind class auditi,
  accessibility (a11y), performance, console xətaları, N+1 query problemi, horizontal scroll
  yoxlaması və vizual sınıqlıq analizi. Tetikleyicilər: "frontend audit et", "mobil yoxla",
  "responsive yoxla", "UI audit", "keyfiyyət audit", "quality audit", "accessibility yoxla",
  "performance yoxla", "konsol xətalarını yoxla", "N+1 query yoxla", "horizontal scroll var?",
  "audit et", "code review", "template yoxla", "UI review".
---

# Frontend Keyfiyyət Auditi — Q360

Bu skill Q360 layihəsinin frontend keyfiyyətini sistematik olaraq auditləyir.
Hər yeni modul tikildikdən sonra (Claude.md-dəki Faza C) bu audit tətbiq olunmalıdır.

## Audit Mərhələləri

### Mərhələ 1: Mobil Responsive Audit (375px / 768px / 1440px)

Hər səhifəni 3 breakpoint-də yoxla:

| Breakpoint | Cihaz | Yoxlanılacaqlar |
|------------|-------|-----------------|
| 375px | iPhone SE | Horizontal scroll olmamalı, tap target ≥ 44px, text oxunaqlı |
| 768px | iPad | Grid 1-2 sütuna düşməli, sidebar collapse olmalı |
| 1440px | Desktop | Tam layout, sidebar açıq |

**Kritik Yoxlamalar:**

- [ ] Horizontal scroll yoxdur (bütün breakpoint-lərdə)
- [ ] `overflow-x: hidden` body-yə əlavə edilib
- [ ] Cədvəllər `overflow-x-auto` wrapper-da
- [ ] Formlar mobil-də full-width
- [ ] Tap target minimum 44x44px
- [ ] Font-size minimum 14px (mobil)
- [ ] Sidebar mobil-də collapse/hamburger menü
- [ ] Modal/dialog mobil-də düzgün ölçüdə

### Mərhələ 2: Console Xətaları

```bash
# Bütün səhifələri scan et
docker compose exec web python test_all_pages.py
```

**Yoxlanılacaqlar:**

- [ ] JavaScript konsol xətası yoxdur
- [ ] 404 resurs istəyi yoxdur (şəkil, CSS, JS faylları)
- [ ] Mixed content xəbərdarlığı yoxdur
- [ ] CSP (Content Security Policy) pozuntusu yoxdur

### Mərhələ 3: N+1 Query Audit

```bash
# Hər səhifə üçün query sayını yoxla
docker compose exec web python show_dup_queries.py /<page-url>/
```

**Qaydalar:**

- Səhifə başına ≤ 15 SQL query
- Eyni cədvələ ≥ 3 eyni query → N+1 problem var
- `select_related()` / `prefetch_related()` istifadə et

**Düzəltmə Pattern-i:**

```python
# YANLIŞ — N+1
items = MyModel.objects.all()
for item in items:
    print(item.created_by.username)  # Hər iterasiyada ayrı query

# DOĞRU — Optimized
items = MyModel.objects.select_related('created_by').all()
```

### Mərhələ 4: TailwindCSS Audit

**Yoxlanılacaqlar:**

- [ ] Inline CSS yoxdur (`style="..."` atributu)
- [ ] Inline JS minimum səviyyədədir
- [ ] Dark mode: hər `bg-white` üçün `dark:bg-gray-800` var
- [ ] Focus ring: interaktiv elementlərdə `focus:ring-*` var
- [ ] Hover state: düymə və linklərdə `hover:*` var
- [ ] Transition: hover effektləri `transition` ilə hamarlaşdırılıb

**Inline JS Yoxlaması:**

```bash
python check_inline_js.py /page-url-1/ /page-url-2/
```

### Mərhələ 5: Accessibility (a11y)

- [ ] Bütün `<img>`-lərdə `alt` atributu var
- [ ] Form elementlərində `<label>` var
- [ ] Kontrast nisbəti WCAG AA (4.5:1 text, 3:1 large text)
- [ ] Keyboard navigation işləyir (Tab, Enter, Escape)
- [ ] ARIA atributları düzgündür
- [ ] Heading hierarchy (H1 → H2 → H3) pozulmayıb
- [ ] Bir səhifədə yalnız 1 `<h1>` var

### Mərhələ 6: Performance

**Yoxlanılacaqlar:**

- [ ] Şəkillərin ölçüsü optimize olunub (WebP/AVIF)
- [ ] Lazy loading: off-screen şəkillər `loading="lazy"`
- [ ] CSS/JS bundle size reasonable
- [ ] Cache headers düzgündür
- [ ] Gzip/Brotli compression aktiv

**Lighthouse Audit:**

```bash
# Docker daxilində
node_modules/.bin/lighthouse http://localhost:8000/<page>/ --output json
```

## Audit Hesabat Formatı

Hər audit bitdikdə `audit_report_<date>.md` faylı yarat:

```markdown
# Frontend Audit Report — YYYY-MM-DD

## Xülasə
- Yoxlanılan səhifə sayı: XX
- PASS: XX
- FAIL: XX
- Kritik problemlər: XX

## Tapıntılar

### 🔴 Kritik (dərhal düzəlt)
| # | Səhifə | Problem | Kateqoriya |
|---|--------|---------|------------|
| 1 | /my-page/ | Horizontal scroll 375px | Responsive |

### 🟡 Orta (planlı düzəlt)
| # | Səhifə | Problem | Kateqoriya |
|---|--------|---------|------------|

### 🟢 Aşağı (nice-to-have)
| # | Səhifə | Problem | Kateqoriya |
|---|--------|---------|------------|

## Səhifə-by-Səhifə Nəticələr
| Səhifə | Responsive | Console | N+1 | a11y | Performance | Status |
|--------|-----------|---------|-----|------|-------------|--------|
```

## Avtomatik Test Script

Bütün səhifələri 200 status ilə yoxlamaq üçün:

```bash
docker compose exec web python smoke_new_pages.py
```

Bu script `urls_batch*.txt` fayllarındakı URL-ləri oxuyur və hər birini test edir.
