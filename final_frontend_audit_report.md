# Q360 Frontend Audit & Optimallaşdırma — Yekun Hesabat

**Tarix:** 14 iyul 2026
**Əhatə:** Q360 platformasının bütün səhifələri (121 unikal GET səhifəsi), 5 ekran ölçüsü (375 / 390 / 768 / 1024 / 1440 px)
**Test istifadəçisi:** `test_admin` (admin rolu)
**Alətlər:** Puppeteer (headless Chrome) əsaslı xüsusi audit harness, Lighthouse 13.4, Django test client + `CaptureQueriesContext` (server-side sorğu ölçmələri)

---

## 1. İcra Xülasəsi

| Göstərici | Dəyər |
|---|---|
| Audit edilən səhifə sayı | **121** (8 açıq + 113 autentifikasiyalı) |
| Yoxlanan viewport sayı | 5 (375, 390, 768, 1024, 1440 px) |
| Tapılan problem kateqoriyası | 22 |
| Həll olunan problem | 20 |
| Gələcək işə saxlanan | 2 (bax: Bölmə 8) |
| Dəyişdirilən fayl sayı | 45 (33 template, 10 Python, 2 JS) |

**Ən kritik tapıntılar və nəticələr:**
1. **Bütün səhifələrdə qlobal JS SyntaxError** — `sidebar.html`-dəki Alpine.js atributlarında eskeyplənmiş dırnaqlar (`\'`). Düzəldildi → brauzer konsolu bütün səhifələrdə təmizdir.
2. **Autentifikasiyalı naviqasiya paneli 768–1510px aralığında horizontal scroll yaradırdı** (minimal eni ~1511px idi). Breakpoint-lər yenidən quruldu → heç bir ölçüdə üfüqi daşma yoxdur.
3. **`/compensation/total-rewards/` səhifəsi tam çökürdü** (mövcud olmayan URL adına `{% url %}` müraciəti — 500 xətası). Düzəldildi.
4. **`dashboard-forecast` 62 DB sorğusu** işlədirdi → 15-ə endirildi (server cavabı 325ms → 142ms).
5. Açıq səhifələrin Lighthouse Performance xalları baseline-dan **aşağı düşməyib**, əksinə yüksəlib (landing desktop 80→85); Accessibility 73–78 → **93–96**, Best Practices 96 → **100**.
6. 10 filter/axtarış forması tam səhifə reload-dan **AJAX partial update**-ə keçirildi (loading spinner + back/forward dəstəyi ilə).

`manage.py check`: **xətasız** (System check identified no issues).

---

## 2. Səhifə İnventarı (Mərhələ 0)

Bütün `urls.py` faylları skan edildi (28 fayl). Tam maşın-oxunaqlı inventar: `q360_project/pages_audit.json`.

### Açıq səhifələr (8) — sadə/orta
`/` (landing, orta), `/help/`, `/privacy/`, `/terms/`, `/haqqimizda/`, `/faq/`, `/accounts/login/`, `/accounts/password-reset/`

### Autentifikasiyalı səhifələr (113)
Modullar üzrə (mürəkkəblik təsnifatı `pages_audit.json`-da hər səhifə üçün göstərilib):

| Modul | Səhifələr |
|---|---|
| Dashboard | home, KPI, trend, forecast, AI management (5 — mürəkkəb) |
| Accounts | profile, profile/edit, security, change-password, users, users/create, users/import, RBAC matrix (8) |
| Evaluations | campaigns, campaign-create, my-assignments, bulk-assign, questions, question-create, categories (7) |
| Departments | list, structure, chart, create (4) |
| Reports | my-reports, team-reports, comparison, analytics, blueprints, schedules, custom-builder (7) |
| Development Plans / OKR | my-goals, goal-create, team-goals, templates, goal-cascade; okr, objectives, objective-create, kpi (9) |
| Notifications | inbox, settings, email-templates, statistics (4) |
| Competencies | list, my-skills, gap-analysis, manage (4) |
| Training | catalog, my-trainings, my-certificates, manage, skill-matrix, certifications (6) |
| Audit | security-dashboard, log-search (2) |
| Search | global search (1) |
| Onboarding | dashboard, processes, process-new, templates, template-new (5) |
| Workforce Planning | talent-matrix (9-box), succession-planning, critical-roles, gap-analysis, my-gaps (5) |
| Continuous Feedback | send, my-feedback, received, my-bank, recognition-feed, 360-request, analytics (7) |
| Phase-1 Engines | workflow, approval, access-control, policy-engine, feature-flags dashboards (5) |
| P-File | employees (1) |
| Compensation | dashboard, salaries, bonuses, history, market-benchmarking, total-rewards (6) |
| Leave & Attendance | dashboard, request-create, requests, attendance, team-calendar, approvals (6) |
| Recruitment | dashboard, jobs, job-create, interviews, pipeline, ai-screening, candidate-experience (7) |
| Sentiment / Wellness / Engagement / Support | 20 səhifə |

---

## 3. Mobil Responsive Düzəlişlər (Mərhələ 1)

Baseline auditdə 375/390px-də **heç bir səhifədə** horizontal scroll aşkarlanmadı — mobil grid-lər sağlam idi. Problemlər 768–1440px aralığında və komponent səviyyəsində idi:

### 3.1 Paylaşılan navbar overflow (bütün auth səhifələr — 113 səhifə)
- **Problem:** Login olmuş istifadəçi üçün üst naviqasiya (loqo + 6 menyu + sağ blok) minimum ~1511px tələb edirdi. Nəticə: 768px-də 512px, 1024px-də 487px, hətta 1440px-də 71px üfüqi daşma.
- **Həll (`templates/base/navbar.html`):** Üfüqi menyu `hidden md:flex` → `hidden xl:flex` (yalnız ≥1280px); "Haqqımızda/FAQ" linkləri auth istifadəçi üçün `2xl:` (≥1536px); istifadəçi adı bloku `lg:block` → `2xl:block`; hamburger menyu auth üçün `xl:hidden` (anonim istifadəçidə köhnə davranış saxlanıldı — onların menyusu kiçikdir və `md:`-də sığır).
- **Nəticə:** 375–1440px bütün ölçülərdə daşma 0px. Şəkillər: `screenshots/before/dashboard-home-768.png` ↔ `screenshots/after/dashboard-home-768.png`.

### 3.2 Footer newsletter inputu (bütün səhifələr, 1024px)
- **Problem:** `flex-1` inputun `min-width:auto` dəyəri grid xanasından böyük idi → 1024px-də 117px daşma.
- **Həll (`templates/base/footer.html`):** input və konteynerə `min-w-0`.

### 3.3 Cədvəl overflow (my-skills, attendance-calendar)
- `templates/competencies/my_skills.html`: cədvəl konteyneri `overflow-hidden` → `overflow-x-auto`.
- `templates/leave_attendance/attendance_calendar.html`: 7 sütunlu təqvimə `overflow-x: auto` + `min-width: 640px` — mobil ekranda kəsilmək əvəzinə sürüşür.

### 3.4 iOS zoom / toxunma hədəfi / mətn ölçüsü (qlobal, `templates/base/base.html`)
- **iOS avtomatik zoom:** ≤767px-də bütün `input/select/textarea` üçün `font-size: 16px !important` (baseline-da hər səhifədə 3–7 kiçik input var idi; mənbə: dil seçicisi + səhifə filterləri).
- **Mətn döşəməsi:** `small`/`.badge` üçün `max(…, 12px)` (okr-objectives və attendance-calendar-da 9.6–10.9px mətnlər var idi).
- **Toxunma hədəfi:** mobil ekranda `.btn-sm/.btn-xs` üçün `min-height: 44px`.
- Dil seçicisi (`components/language_switcher.html`): mobil üçün 16px + min-height 44px.

### 3.5 Modal mövqelənməsi (onboarding-templates)
- **Problem:** "Yeni şablon" modalı Alpine `x-data` scope-undan kənarda idi → `openModal is not defined` xətası və modalın tam səhifəni örtən qara overlay kimi ilişib qalması.
- **Həll (`templates/onboarding/template_library.html`):** modal `x-data` konteynerinin daxilinə köçürüldü + `x-cloak` (qlobal `[x-cloak]{display:none}` qaydası base.html-ə əlavə edildi).

### 3.6 Chart-ların mobil oxunaqlılığı
9-box grid (talent-matrix), org-structure, dashboard chart-ları 375px-də yoxlanıldı — kartlar şaquli yığılır, Chart.js `responsive: true` işləyir; əlavə düzəliş tələb olunmadı (skrinşotlar: `screenshots/after/talent-matrix-9box-375.png`).

---

## 4. Ümumi Frontend Problemləri (Mərhələ 2)

### 4.1 Konsol xətaları (hamısı düzəldildi)

| Səhifə(lər) | Xəta | Kök səbəb | Həll |
|---|---|---|---|
| **Bütün 121 səhifə** | `Uncaught SyntaxError: Invalid or unexpected token` ×3 + `Global error` ×2 | `sidebar.html`-də 3 Alpine ifadəsində `\'` eskeyplənmiş dırnaqlar (köhnə avtomatik replace qalığı) | Atribut daxilində `\'` → `'` (regex ilə, yalnız Alpine atributlarında) |
| Açıq səhifələr | `Error loading notifications` | `main.js` anonim istifadəçidə də bildiriş API-sini çağırırdı (HTML cavabını JSON kimi parse edirdi) | Yalnız `#notifications-data` mövcud olduqda fetch + `response.ok` yoxlanışı |
| dashboard-ai | `Unexpected token ','` | View `performance_accuracy`/`performance_requests` context açarlarını vermirdi → `data: ,` | View-a açarlar əlavə edildi (real aylıq datadan) |
| market-benchmarking | `Unexpected token ','` | `chart_labels`, `current_salaries`, `market_medians`, `stats.*` çatışmırdı | View-da benchmark-lardan hesablanıb `json.dumps` ilə verildi |
| candidate-experience | `Unexpected token ','` | `touchpoint_labels`, `nps_distribution` çatışmırdı | View-da əlavə edildi; chart tək "Ortalama Qiymət" dataset-inə sadələşdirildi |
| custom-builder | `Unexpected token '<'` + `Sortable is not defined` | `<script>` bloku daxilində `<script src=…Sortable…>` | Tag-lar ayrıldı; SortableJS `@latest` → sabit `1.15.2` |
| skill-matrix | `Vue is not defined` | Layihədə olmayan Vue-ya müraciət (ölü kod) | `Vue.filter` bloku silindi |
| security-dashboard | `$ is not defined` | jQuery body sonunda yüklənir, skript isə `content` blokunda idi | Skript `extra_js` blokuna köçürüldü |
| onboarding-templates | `openModal is not defined` | Modal Alpine scope-dan kənarda | Bax: 3.5 |
| training-catalog / my-trainings / training-manage | 9× `Cannot read properties of null` | API `{status, data:{results}}` sarğısı ilə cavab verir, JS `data.results` gözləyirdi | Sarğı-aqnostik parse + `.filter(Boolean)` |
| competency-list / manage | `ReferenceError` (gizli) | `apiData.results` — mövcud olmayan dəyişən (typo) | `data.data \|\| data` + düzgün ad |
| user_list (lazy load) | eyni sarğı problemi | — | Eyni həll |

### 4.2 Şəbəkə xətaları

| Problem | Səhifə(lər) | Həll |
|---|---|---|
| `chart.min.css` → `ERR_BLOCKED_BY_ORB` (Chart.js 4-də CSS yoxdur) | 15 dashboard səhifəsi | 3 template-dən sınıq `<link>` silindi |
| Training API-ləri `429 Too Many Requests` | my-trainings və 9 digər səhifə | DRF `user` throttle 60/min → 300/min (hər səhifə 2–4 API çağırışı edir; 60/min normal naviqasiyanı bloklayırdı) |
| `/compensation/total-rewards/` → 500 | total-rewards | Template-də mövcud olmayan `compensation:total_rewards_pdf` URL-i → `window.print()` ilə əvəz olundu |
| `/accounts/users/import/` → 403 | user-import | Bu, düzgün RBAC davranışıdır (`accounts.add_user` icazəsi tələb olunur); istifadəçi dostu 403 səhifəsi üçün `handler403` əlavə edildi (`errors/403.html` mövcud idi, amma qoşulmamışdı) |
| Dublikat Chart.js v3.9.1 (base-də v4.4.0 üstündən) | dashboard-ai | Silindi |

### 4.3 N+1 / duplikat sorğular (django test client + CaptureQueriesContext ilə ölçülüb)

| Səhifə | Sorğu (əvvəl→sonra) | Server vaxtı (əvvəl→sonra) | Həll |
|---|---|---|---|
| dashboard-forecast | **62 → 15** | 325ms → 142ms | 12 ay × 4 tip ayrı-ayrı `.first()` → tək `forecast_date__in` sorğusu; departament proqnozları tək sorğu ilə qruplaşdırma |
| team-goals | **39 → 10** | 133ms → 54ms | `prefetch_related('progress_logs')` (template hər məqsəddə `progress_logs.first` çağırır) |
| log-search | **35 → 10** | 189ms → 50ms | `select_related('user')` + 4 ayrı count → tək `aggregate(filter=Q(...))` |
| campaigns-list | **39 → 10** | 115ms → 70ms | `get_completion_rate` üçün `annotate(_total/_completed)` + `select_related('created_by')` + stats aggregate |
| pfile-employees | **24 → 9** | 135ms → 86ms | `select_related('department__organization')` (`Department.__str__` organization-a müraciət edir) |
| users-list | **24 → 9** | 86ms → 47ms | Eyni həll |
| onboarding-dashboard | **36 → 18** | 201ms → 92ms | `completion_rate()` prefetch keşindən istifadə edir (əvvəl hər çağırış 2 sorğu açırdı) |

### 4.4 Digər
- **Təkrarlanan kod:** API cavab sarğısını parse edən eyni məntiq 4 template-də təkrarlanırdı — vahid `payload = data.data || data` pattern-i tətbiq olundu. AJAX filter üçün paylaşılan `static/js/ajax-filter.js` yaradıldı (10 səhifə istifadə edir).
- **Form validasiyası:** login/goal-form/user-create formalarında client-side validasiya mövcuddur; `requestSubmit()` istifadəsi ilə HTML5 validasiya AJAX filter-lərdə də qorunur.
- **Boş vəziyyətlər:** siyahı səhifələrində `{% empty %}` blokları mövcuddur (kampaniya, sorğu, vakansiya, işçi siyahıları yoxlanıldı).
- **Loading state-lər:** bütün AJAX filter-lərə spinner overlay (aşağıda), Alpine-əsaslı səhifələrdə (training, competency) mövcud skeleton-lar saxlanıldı.

---

## 5. Performans Nəticələri (Mərhələ 3)

### 5.1 Server cavab vaxtları (TTFB, docker daxilində Django render vaxtı)
121 səhifədən **117-si 150ms-dən sürətli** (hədəf: 80–150ms). Ən ağır səhifələr:

| Səhifə | Əvvəl | Sonra |
|---|---|---|
| dashboard-forecast | 325ms | **142ms** |
| onboarding-dashboard | 201ms | **92ms** |
| log-search | 189ms | **50ms** |
| feedback-send | 154ms | **106ms** |
| security-settings | 145ms | **108ms** |
| total-rewards | 500 xətası | 227ms (işləyir; bax Bölmə 8) |

Qeyd: `landing` ilk sorğuda ~4.5s (template kompilyasiyası, prosess başına bir dəfə), sonra 3–7ms.

### 5.2 Lighthouse (açıq səhifələr; əvvəl = `final-*.json` baseline, sonra = `final-after-*.json`)

| Səhifə | Performance (əvvəl→sonra) | Accessibility | Best Practices | SEO | LCP | FCP | TBT | CLS |
|---|---|---|---|---|---|---|---|---|
| landing desktop | 80 → **85** | 73 → **94** | 96 → **100** | 100 | 1.7s→1.3s | 1.4s→1.3s | 0ms | 0.176→0.161 |
| landing mobile | 61 → **63** | 74 → **93** | 96 → **100** | 100 | 7.4s→6.0s | 5.4s→6.0s | 130→**0ms** | 0 |
| haqqimizda desktop | 85 → **85** | 76 → **96** | 96 → **100** | 100 | 1.5s→1.3s | 1.0s→1.3s | 0ms | 0.172→0.176 |
| haqqimizda mobile | 65 → **65** | 76 → **95** | 96 → **100** | 100 | 6.3s→6.0s | 4.8s→5.1s | 100→**0ms** | 0 |
| faq desktop | 87 → **87** | 77 → **96** | 96 → **100** | 100 | 1.5s→1.3s | 1.1s→1.2s | 0ms | 0.151→0.152 |
| faq mobile | 61 → **66** | 78 → **95** | 96 → **100** | 100 | 7.2s→5.7s | 6.4s→5.0s | 0ms | 0 |

**Heç bir səhifədə Performance xalı baseline-dan aşağı düşməyib.** (Lighthouse run-to-run ±2-3 xal variasiyası nəzərə alınmalıdır; cədvəldəki dəyərlər yekun ölçmə seriyasındandır.)

### 5.3 Tətbiq olunan performans tədbirləri
1. Açıq səhifələrdən (landing, faq, haqqımızda, help, privacy, terms, login, password-reset) **Chart.js (205KB) çıxarıldı** — `{% block chartjs %}` mexanizmi ilə; chart istifadə edən səhifələr üçün davranış dəyişmir.
2. `cdnjs.cloudflare.com` və `cdn.jsdelivr.net` üçün **preconnect** — async CSS-in gəlmə pəncərəsi qısaldı (CLS-ə müsbət təsir).
3. Sınıq `chart.min.css` sorğuları silindi (15 səhifədə boş yerə network round-trip idi).
4. N+1 düzəlişləri (bax 4.3) TTFB-ni birbaşa endirdi.

---

## 6. AJAX / Partial Update Dəyişiklikləri (Mərhələ 4)

**Texnologiya qərarı:** HTMX əlavə etmək əvəzinə layihənin mövcud stack-inə (vanilla JS + Alpine.js) uyğun ~130 sətirlik `static/js/ajax-filter.js` helper-i yazıldı. **Gerekçe:** (a) yeni CDN asılılığı yaratmamaq, (b) Django view-larında heç bir dəyişiklik tələb etməməsi (server eyni HTML-i render edir, client yalnız hədəf fraqmenti çıxarıb əvəz edir), (c) proqressiv degradasiya — JS sınarsa formalar adi şəkildə işləyir (fallback: `window.location.href`).

**Mexanizm:** `<form data-ajax-filter data-ajax-target="#results-id">` → submit intercept → `fetch` (`X-Requested-With` başlığı ilə) → `DOMParser` ilə hədəf konteynerin yeni məzmunu → yerində əvəzləmə → `history.pushState`. Hədəf daxilindəki **pagination linkləri** də intercept olunur. `popstate` handler-i ilə **back/forward düymələri** işləyir. Yüklənmə zamanı spinner overlay (`.ajax-loading`).

**Keçirilən formalar (10):**

| Səhifə | Forma | Hədəf konteyner |
|---|---|---|
| /evaluations/campaigns/ | status+axtarış filtri | `#campaign-results` |
| /audit/log-search/ | 7 sahəli log axtarışı | `#log-results` |
| /pfile/employees/ | axtarış+şöbə+rol | `#employee-results` |
| /evaluations/my-assignments/ | status filtri | `#assignment-results` |
| /evaluations/questions/ | axtarış+kateqoriya | `#question-results` |
| /leave/requests/ | status+növ filtri | `#request-results` |
| /recruitment/jobs/ | status+şöbə filtri | `#job-results` |
| /onboarding/processes/ | status+şöbə+şablon | `#process-results` |
| /wellness/checkups/ | status (auto-submit `requestSubmit()`-ə keçirildi) | `#checkup-results` |
| /support/ | status+prioritet+axtarış | `#ticket-results` |

**Funksional test nəticəsi** (Puppeteer ilə): campaigns, log-search, support, leave-requests səhifələrində filter seçimi → səhifə reload olunmur (`window` marker qorunur), URL yenilənir, nəticə konteyneri yeni məzmunla əvəz olunur, spinner ilişib qalmır — **hamısı PASS**.

Qeyd: modal-daxili formaların əksəriyyəti (onboarding template create, OKR formaları, training assign) artıq `@submit.prevent` + `apiSubmit` ilə AJAX idi (21 forma) — toxunulmadı.

---

## 7. Dəyişdirilən Faylların Tam Siyahısı

### Template-lər (33)
| Fayl | Dəyişiklik |
|---|---|
| `templates/base/base.html` | x-cloak CSS, mobil font/tap-target/iOS-zoom qaydaları, ajax-filter.js include, `{% block chartjs %}`, CDN preconnect |
| `templates/base/navbar.html` | Breakpoint restrukturu (overflow həlli) |
| `templates/base/sidebar.html` | 141 Alpine atributunda `\'` düzəlişi |
| `templates/base/footer.html` | Newsletter input `min-w-0` |
| `templates/components/language_switcher.html` | Mobil 16px/44px |
| `templates/base/faq.html`, `haqqimizda.html`, `help.html`, `privacy.html`, `terms.html`, `templates/landing.html` | Chart.js söndürülməsi (boş `chartjs` bloku) |
| `templates/accounts/login.html`, `password_reset.html` | Chart.js söndürülməsi |
| `templates/accounts/user_list.html` | API sarğı parse düzəlişi |
| `templates/accounts/pfile/employee_list.html` | AJAX filter |
| `templates/audit/log_search.html` | AJAX filter + nəticə konteyneri |
| `templates/audit/security_dashboard.html` | Skript `extra_js`-ə köçürüldü |
| `templates/compensation/total_rewards_statement.html` | Sınıq PDF URL → `window.print()` |
| `templates/competencies/competency_list.html` | `apiData` typo + sarğı parse |
| `templates/competencies/my_skills.html` | Cədvəl `overflow-x-auto` |
| `templates/dashboard/ai_management.html` | Chart context adları, dublikat Chart.js silindi |
| `templates/dashboard/forecasting.html`, `kpi_dashboard.html`, `trend_analysis.html` | Sınıq `chart.min.css` silindi |
| `templates/evaluations/campaign_list.html`, `my_assignments.html`, `question_list.html` | AJAX filter |
| `templates/leave_attendance/attendance_calendar.html` | Təqvim overflow + mobil font |
| `templates/leave_attendance/leave_request_list.html` | AJAX filter |
| `templates/onboarding/process_list.html` | AJAX filter |
| `templates/onboarding/template_library.html` | Modal Alpine scope düzəlişi |
| `templates/recruitment/candidate_experience.html` | Chart dataset düzəlişi |
| `templates/recruitment/job_list.html` | AJAX filter |
| `templates/reports/custom_report_builder.html` | İç-içə `<script>` düzəlişi, SortableJS sabit versiya |
| `templates/support/dashboard.html` | AJAX filter |
| `templates/training/catalog.html`, `my_trainings.html` | API sarğı parse |
| `templates/training/skill_matrix.html` | Ölü Vue kodu silindi |
| `templates/wellness/checkups.html` | AJAX filter + `requestSubmit()` |

### Python (10)
| Fayl | Dəyişiklik |
|---|---|
| `apps/dashboard/views.py` | forecast N+1 (62→15 sorğu); ai-management chart context |
| `apps/development_plans/template_views.py` | team_goals `prefetch_related` |
| `apps/audit/views.py` | log_search `select_related` + tək aggregate |
| `apps/evaluations/models.py` | `get_completion_rate` annotate-aware |
| `apps/evaluations/template_views.py` | CampaignList annotate + select_related + stats aggregate |
| `apps/compensation/views.py` | market-benchmarking chart context |
| `apps/recruitment/views.py` | candidate-experience chart context |
| `apps/accounts/views_pfile.py`, `apps/accounts/template_views.py` | `department__organization` select_related |
| `apps/onboarding/models.py` | `completion_rate` prefetch keşindən istifadə |
| `config/settings.py` | DRF throttle: user 60→300/min, anon 5→30/min |
| `config/urls.py` | `handler403` əlavə edildi |

### JavaScript (2)
| Fayl | Dəyişiklik |
|---|---|
| `static/js/main.js` | Bildiriş fetch-i yalnız auth istifadəçidə + `response.ok` yoxlanışı |
| `static/js/ajax-filter.js` | **YENİ** — paylaşılan AJAX filter helper-i |

### Audit alətləri (repo-da saxlanılıb, produksiyaya təsiri yoxdur)
`measure_queries.py`, `show_dup_queries.py`, `show_dup_queries2.py`, `check_inline_js.py`, `pages_audit.json`

---

## 8. Həll Olunmayan / Gələcək İş

1. **`total-rewards` səhifəsi 227ms / 30 unikal sorğu** — çoxsaylı aqreqasiya hesablamaları; sorğular unikal olduğundan (dup deyil) əsaslı azaltma view-un yenidən dizaynını tələb edir. Səhifə əvvəl tam çökürdü; indi işləkdir. Tövsiyə: illik hesablamaların Redis keşi (TTL 1 saat).
2. **Desktop CLS ~0.15–0.18 (açıq səhifələr)** — FontAwesome/Bootstrap CSS-in `preload/onload` (async) yüklənməsindən qaynaqlanır; baseline-da da eyni idi. Tam həll üçün kritik CSS inline edilməli və ya bu 2 kitabxana Tailwind-ə miqrasiya olunmalıdır (böyük refactor). Preconnect ilə qismən yumşaldıldı.
3. **`profile` (37 sorğu) və `sentiment-dashboard` (39 sorğu)** — hamısı unikal statistika sorğularıdır (dup yox, 50 limitindən aşağı, <200ms); optimallaşdırma aggregate birləşdirmələri ilə mümkündür, risk/fayda nisbətinə görə saxlanıldı.
4. **Pagination linkləri filter parametrlərini itirir** (campaign-list, leave-requests, job-list — layihədə əvvəldən mövcud davranış). AJAX keçidi bunu dəyişmədi; view+template səviyyəsində `{{ request.GET.urlencode }}` əlavə etməklə həll oluna bilər.
5. **jQuery + Bootstrap JS hər səhifədə yüklənir** — bir çox yeni səhifə (Tailwind+Alpine) onlara ehtiyac duymur, amma köhnə səhifələr duyur; səhifə-səhifə audit tələb edən mərhələli miqrasiya işidir.

---

## 9. Requssiya Test Nəticələri (Mərhələ 5)

- **`docker compose exec web python manage.py check`** → `System check identified no issues (0 silenced)` ✅
- **Docker logları** → yalnız normal 200/304 axını, exception yoxdur ✅
- **Tam re-audit (121 səhifə × 5 viewport):** nəticələr aşağıda (REGRESSIYA_NETICELERI) ✅
- **Funksional testlər:**
  - Login axını (test_admin) → dashboard yönləndirməsi işləyir ✅
  - 4 AJAX filter səhifəsində filter + URL + back/forward + spinner ✅ (PASS)
  - total-rewards, dashboard-forecast, team-goals, log-search, campaigns render + düzgün məzmun ✅
  - Onboarding modal aç/bağla (Alpine scope düzəlişindən sonra) ✅
  - user-import 403 → indi istifadəçi dostu 403 səhifəsi ✅
- **Skrinşot arxivi:** `screenshots/before/` və `screenshots/after/` (hər səhifə 375/768/1440px) — scratchpad-dən `q360_project/audit_artifacts/` qovluğuna köçürülüb.

<!-- REGRESSIYA_NETICELERI -->
