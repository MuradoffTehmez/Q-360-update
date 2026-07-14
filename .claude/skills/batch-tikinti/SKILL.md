---
name: batch-tikinti
description: >
  Q360 layihəsində Claude.md-dəki 28 batch-i ardıcıl olaraq tikmək üçün iş axışı bələdçisi.
  Hər batch-in tələblərini, sırasını, yoxlama addımlarını və jurnal formatını təyin edir.
  Tetikleyicilər: "batch tik", "batch X-i tik", "növbəti batch", "bütün batch-ləri tik",
  "yeni səhifələri yarat", "161 səhifəni tik", "Claude.md-dəki planı icra et", "faza B",
  "batch tikintisi", "modul tikintisi davam et", "build modules", "continue building".
---

# Batch Tikinti İş Axışı — Q360

Bu skill Claude.md-dəki 28 batch-in ardıcıl şəkildə tikilməsi üçün iş axışını izah edir.
Hər batch AYRI-AYRI tam bitirilib yoxlanmalıdır.

## Faza A — Konvensiya Öyrənmə (ƏVVƏLCƏ)

Yeni kod yazmazdan əvvəl mövcud 2-3 tam modulu DİQQƏTLƏ oxu:
- `apps/evaluations/` — models, template_views, urls, templates
- `apps/leave_attendance/` — forms, serializers, CRUD pattern
- `apps/core/models.py` — TimeStampedModel, SoftDeletableModel

Bu konvensiyalara BÜTÜN yeni kodda tam əməl et. `q360-konvensiya` skill-inə istinad et.

## Faza B — Batch Sırası (28 batch)

| Batch | Modul | Səhifə Sayı | Qeydlər |
|-------|-------|-------------|---------|
| 1 | Settings | 23 | MFA/SSO → stub |
| 2 | Accounts əlavələri | 7 | |
| 3 | Dashboard əlavələri | 4 | |
| 4 | Evaluations əlavələri | 7 | |
| 5 | Departments əlavələri | 3 | |
| 6 | Reports əlavələri | 4 | |
| 7 | Development Plans əlavələri | 3 | |
| 8 | Notifications əlavələri | 6 | |
| 9 | Competencies əlavələri | 3 | |
| 10 | Training əlavələri | 4 | |
| 11 | Audit əlavələri | 6 | |
| 12 | Workforce Planning əlavələri | 2 | |
| 13 | Feedback əlavələri | 3 | |
| 14 | Workflow | 6 | Designer → stub |
| 15 | Approval əlavələri | 5 | |
| 16 | Access Control əlavələri | 6 | |
| 17 | Policy Engine | 5 | Simulator → stub |
| 18 | Feature Flags əlavələri | 5 | |
| 19 | P-File əlavələri | 6 | |
| 20 | Compensation əlavələri | 4 | |
| 21 | Leave əlavələri | 5 | |
| 22 | OKR əlavələri | 4 | |
| 23 | Recruitment əlavələri | 5 | |
| 24 | Sentiment əlavələri | 3 | |
| 25 | Wellness əlavələri | 3 | |
| 26 | Engagement əlavələri | 3 | |
| 27 | Support əlavələri | 6 | |
| 28 | Yeni top-level modullar | 17 | SUPERUSER-ONLY |

## Hər Batch üçün Minimum Tələb

Hər batch tikildiqdə bu checklist-i keç:

### 1. Model Yaratma
- [ ] `TimeStampedModel`-dən miras alır
- [ ] verbose_name Azərbaycan dilində
- [ ] `created_by` ForeignKey var
- [ ] `STATUS_CHOICES` var (lazım olduqda)
- [ ] `HistoricalRecords()` əlavə olunub (vacib modellərə)

### 2. View Yaratma
- [ ] `template_views.py`-da class-based views
- [ ] `LoginRequiredMixin` var
- [ ] `select_related()` / `prefetch_related()` istifadə olunub
- [ ] `paginate_by` təyin olunub
- [ ] RBAC/permission yoxlaması var

### 3. URL Qeydiyyatı
- [ ] `urls.py`-da `app_name` var
- [ ] `config/urls.py`-da qeydiyyat var
- [ ] Namespace düzgündür

### 4. Template Yaratma
- [ ] `{% extends "base/base.html" %}` ilə başlayır
- [ ] TailwindCSS class-ları ilə stilləndirmə
- [ ] Dark mode dəstəyi (`dark:` prefix)
- [ ] Responsive (375px/768px/1440px)
- [ ] `{% trans %}` ilə i18n
- [ ] Sidebar-da naviqasiya linki əlavə olunub

### 5. Yoxlama
- [ ] `manage.py makemigrations` — uğurlu
- [ ] `manage.py migrate` — uğurlu
- [ ] `manage.py check` — xətasız
- [ ] Səhifə 200 qaytarır (curl/test)
- [ ] Horizontal scroll yoxdur (375px/768px/1440px)
- [ ] Console JS xətası yoxdur

## Batch Jurnal Formatı

Hər batch bitdikdə aşağıdakı formatda qeyd yarat:

```markdown
## Batch X — [Modul Adı] ✅

**Tikilən səhifələr:** X
**Data modelləri:** Model1, Model2, ...
**Yaradılan fayllar:**
- apps/<module>/models.py
- apps/<module>/template_views.py
- apps/<module>/urls.py
- templates/<module>/list.html
- templates/<module>/detail.html
- ...

**STUB/TODO:**
- /path/stub-page/ — "Tezliklə" (real spec tələb edir)

**Yoxlama nəticələri:**
- manage.py check: ✅ xətasız
- migrate: ✅ uğurlu
- 200 status: ✅ bütün URL-lər
- Responsive: ✅ / ⚠️

**Qeydlər:** ...
```

## STUB/Coming Soon Qaydaları

Aşağıdakı səhifələr STUB kimi qeyd olunmalıdır:
- `/settings/mfa/` — MFA inteqrasiyası
- `/settings/sso/` — SSO inteqrasiyası
- `/workflow/designer/` — Sürükle-burax vizual dizayner
- `/policy-engine/simulator/` — Policy simulyasiya mühərriki
- `/ai/models/`, `/ai/prompts/` — LLM provider olmadıqda
- `/system/health/`, `/system/cache/` — Real cache backend olmadıqda

STUB Template Pattern:
```html
{% extends "base/base.html" %}
{% load i18n %}

{% block title %}{% trans "Tezliklə" %} - Q360{% endblock %}

{% block content %}
<div class="flex items-center justify-center min-h-[60vh]">
  <div class="text-center">
    <div class="text-6xl mb-4">🚧</div>
    <h1 class="text-2xl font-bold text-gray-800 dark:text-white mb-2">
      {% trans "Tezliklə" %}
    </h1>
    <p class="text-gray-500 dark:text-gray-400">
      {% trans "Bu funksionallıq hazırlanma mərhələsindədir." %}
    </p>
    <!-- TODO: Real inteqrasiya əlavə olunmalıdır. Spec tələb edir. -->
  </div>
</div>
{% endblock %}
```

## Faza C — Frontend Audit (Batch-lər bitdikdən sonra)

Bütün 161 yeni səhifəyə `frontend-audit` skill-indəki kriteriyaları tətbiq et.

## Faza D — Yekun Hesabat

`final_new_modules_report.md` faylı yarat:
- Hər batch üzrə: tikilən səhifə sayı, data modeli xülasəsi, fayl siyahısı
- STUB/TODO kimi qeyd olunan səhifələrin tam siyahısı
- Naviqasiya strukturu (hansı rol hansı yeni səhifəni görür)
- manage.py check və migration nəticələri
- Mobil/frontend audit nəticələri
- Dəyişdirilən/yaradılan bütün faylların tam siyahısı
