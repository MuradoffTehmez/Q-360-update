# KRİTİK DOĞRULAMA HESABATI — 161 Səhifənin Real Vəziyyəti

**Tarix:** 2026-07-14  
**İcra mühiti:** Docker (`q360_project/`), PostgreSQL 16, Django 5.1.4, DEBUG=True  
**Metod:** Bütün nəticələr Docker `web` konteyneri daxilində real əmr çıxışlarına əsaslanır. Django test client (`force_login`) ilə 161 URL tək-tək sorğulandı. **Heç bir kod dəyişikliyi edilmədi** (yalnız 2 müvəqqəti test istifadəçisi yaradılıb dərhal silindi; `git status` = yalnız bu hesabat faylı).

**Ümumi rəqəm:** 161 URL-dən planlaşdırılan yolda **117 = HTTP 200**, **35 = 404**, **9 = 500**. 28 batch-dan **15 TƏSDİQLƏNDİ**, **13 TƏSDİQLƏNMƏDİ**.

---

## 🔴 0. TƏHLÜKƏSİZLİK NƏTİCƏSİ (PRİORİTET #1 — ƏN BAŞDA)

### 🔴 KRİTİK: RBAC və Policy idarəetmə səhifələri adi istifadəçiyə açıqdır

Batch 14–18 (Workflow, Approval, **Access Control**, **Policy Engine**, Feature Flags) UI səhifələri planlaşdırılan yollarda (`/access-control/roles/`, `/policy-engine/policies/` və s.) **404 verir**, çünki səhv prefiksdə qeydiyyatdadır. Onların FAKTİKİ işləyən nüsxələri `/api/v1/...` altındadır və yalnız `@login_required` ilə qorunur — **superuser/permission yoxlaması YOXDUR** (`apps/*/views_extras.py` — hamısı `@login_required`).

**Test — adi (staff/superuser olmayan) `qa_tmp_regular_sec2` istifadəçisi, tam əmr çıxışı:**

```
$ docker compose exec -T web python - < verify_sec_alt.py
S2|/api/v1/workflow/workflows/|EXC|NoReverseMatch: 'workflow_engine' is not a registered namespace
S2|/api/v1/workflow/designer/|200|
S2|/api/v1/workflow/versions/|200|
S2|/api/v1/workflow/history/|200|
S2|/api/v1/workflow/logs/|200|
S2|/api/v1/workflow/monitoring/|200|
S2|/api/v1/approval/rules/|200|
S2|/api/v1/approval/chains/|200|
S2|/api/v1/approval/history/|200|
S2|/api/v1/approval/queue/|200|
S2|/api/v1/approval/delegations/|200|
S2|/api/v1/access-control/roles/|200|          ← Rolların idarəetmə UI-si
S2|/api/v1/access-control/permissions/|200|    ← İcazələrin idarəetmə UI-si
S2|/api/v1/access-control/policies/|200|
S2|/api/v1/access-control/groups/|200|
S2|/api/v1/access-control/requests/|200|
S2|/api/v1/access-control/history/|200|
S2|/api/v1/policy-engine/policies/|200|         ← Siyasət idarəetmə UI-si
S2|/api/v1/policy-engine/rules/|200|
S2|/api/v1/policy-engine/simulator/|200|
S2|/api/v1/policy-engine/versions/|200|
S2|/api/v1/policy-engine/logs/|200|
S2|/api/v1/feature-flags/flags/|200|
S2|/api/v1/feature-flags/environments/|200|
S2|/api/v1/feature-flags/rollouts/|200|
S2|/api/v1/feature-flags/experiments/|200|
S2|/api/v1/feature-flags/history/|200|
CLEANUP|qa_tmp_regular_sec2 silindi
DONE
```

**27 idarəetmə səhifəsindən 26-sı adi istifadəçiyə HTTP 200 qaytardı** (1-i NoReverseMatch/500). İçində RBAC rol/icazə redaktoru və policy engine idarəetməsi kimi həssas administrativ interfeyslər var. Kök: `apps/access_control/views_extras.py:6` və digər engine `views_extras.py`-larda bütün view `@login_required` işlədir, superuser yoxlaması yoxdur.

### ✅ Qorunan sahələr (təhlükəsizlik testi keçdi) — tam əmr çıxışı

Adi istifadəçi `qa_tmp_regular_161` ilə Batch 1, 16, 17, 28 (54 URL) sorğulandı. Status yekunu:

```
=== S statusları ===
     43 302   (login/dashboard-a yönləndirmə — qorunur)
     11 404   (access-control/* və policy-engine/* planlaşdırılan yollar — mövcud deyil)
      0 200   (icazəsiz giriş YOXDUR)

=== S: 200 qaytaranlar (KRİTİK) ===
(nəticə yoxdur — heç bir səhifə açıq deyil)

=== S: 302 nümunə ===
S|/settings/|302|/dashboard/
S|/settings/general/|302|/dashboard/
S|/settings/localization/|302|/dashboard/
S|/settings/languages/|302|/dashboard/
S|/settings/timezone/|302|/dashboard/

=== S: 404 (access-control/* və policy-engine/* planlaşdırılan yollar) ===
S|/access-control/roles/|404|
S|/access-control/permissions/|404|
S|/access-control/policies/|404|
S|/access-control/groups/|404|
S|/access-control/access-requests/|404|
S|/access-control/access-history/|404|
S|/policy-engine/policies/|404|
S|/policy-engine/rules/|404|
S|/policy-engine/simulator/|404|
S|/policy-engine/versions/|404|
S|/policy-engine/logs/|404|
```

- **Batch 28** (`/files/`, `/ai/`, `/system/`, `/imports/`, `/exports/`, `/admin-panel/*` — 19 URL): adi istifadəçi → **302** (login-ə yönləndirmə). `@superuser_required` düzgün tətbiq olunub (`apps/superuser_tools/views.py:5-12`). ✅
- **Batch 1** (`/settings/*` — 24 URL): adi istifadəçi → **302 → /dashboard/** (icazə yoxlaması redirect edir). ✅ (Spec 403 istəyirdi, faktiki 302-dir — qorunur, status kodu fərqlidir.)
- **Batch 16/17 planlaşdırılan yollar** (11 URL): hamıya 404 (o prefiksdə səhifə yoxdur — yuxarıdakı kritik tapıntıya bax).

**Yekun:** Superuser-only `/files/`, `/ai/`, `/system/`, `/admin-panel/`, `/settings/*` düzgün qorunur. LAKİN Access Control və Policy Engine idarəetmə səhifələri (`/api/v1/...`) adi istifadəçiyə açıqdır — **kritik təhlükəsizlik problemidir, düzəliş tələb edir.**

---

# FAZA 1 — KÖK SƏBƏB DİAQNOZU (hər addımın tam əmr çıxışı ilə)

## Addım 1.1 — Fayllar həqiqətən mövcuddurmu? BƏLİ

**Əmr:** `find apps/ -maxdepth 1 -type d -newer manage.py`

```
apps/
apps/access_control      apps/accounts          apps/approval_engine   apps/audit
apps/compensation        apps/competencies      apps/continuous_feedback  apps/core
apps/dashboard           apps/departments       apps/development_plans  apps/engagement
apps/evaluations         apps/feature_flags     apps/leave_attendance   apps/notifications
apps/onboarding          apps/performance_reviews  apps/policy_engine   apps/recruitment
apps/reports             apps/search            apps/sentiment_analysis apps/superuser_tools
apps/support             apps/system_settings   apps/training           apps/wellness
apps/workflow_engine     apps/workforce_planning
```

**Əmr:** hər yeni app üçün `ls -la apps/<app>/` (əsas fayllar):

```
apps/system_settings   : __init__.py admin.py apps.py migrations/ models.py(1936B) registry.py(8582B) urls.py views.py
apps/superuser_tools   : __init__.py admin.py apps.py migrations/ models.py(57B) tests.py urls.py(1488B) views.py(3394B)
apps/workflow_engine   : admin.py apps.py migrations/ models.py(7020B) serializers.py services.py template_views.py ui_urls.py urls.py views.py views_extras.py
apps/approval_engine   : admin.py apps.py migrations/ models.py(4622B) serializers.py services.py template_views.py ui_urls.py urls.py views.py views_extras.py
apps/access_control    : admin.py apps.py migrations/ models.py(5111B) permissions.py serializers.py services.py template_views.py ui_urls.py urls.py views.py views_extras.py
apps/policy_engine     : admin.py apps.py migrations/ models.py(3011B) serializers.py services.py template_views.py ui_urls.py urls.py views.py views_extras.py
apps/feature_flags     : admin.py apps.py decorators.py migrations/ models.py(4086B) serializers.py services.py template_views.py ui_urls.py urls.py views.py views_extras.py
apps/support           : admin.py api_views.py apps.py migrations/ models.py(4306B) serializers.py tests.py urls.py views.py views_extras.py
apps/engagement        : admin.py api.py apps.py forms.py management/ migrations/ models.py(17236B) serializers.py services.py tests/ urls.py views.py views_extras.py
apps/wellness          : admin.py api_views.py apps.py forms.py migrations/ models.py(22505B) serializers.py services.py templatetags/ tests.py urls.py views.py views_extras.py
apps/sentiment_analysis: __init__.py api_views.py apps.py migrations/ models.py(3213B) serializers.py services.py templates/ tests.py urls.py views.py views_extras.py
```

**Əmr (konteyner daxili — volume mapping yoxlaması):** `docker compose exec -T web sh -c "find /app/apps -maxdepth 1 -type d | sort"`

```
/app/apps  /app/apps/access_control  /app/apps/accounts  /app/apps/approval_engine
/app/apps/audit  /app/apps/compensation  /app/apps/competencies  /app/apps/continuous_feedback
/app/apps/core  /app/apps/dashboard  /app/apps/departments  /app/apps/development_plans
/app/apps/engagement  /app/apps/evaluations  /app/apps/feature_flags  /app/apps/leave_attendance
/app/apps/notifications  /app/apps/onboarding  /app/apps/performance_reviews  /app/apps/policy_engine
/app/apps/recruitment  /app/apps/reports  /app/apps/search  /app/apps/security
/app/apps/sentiment_analysis  /app/apps/superuser_tools  /app/apps/support  /app/apps/system_settings
/app/apps/training  /app/apps/wellness  /app/apps/workflow_engine  /app/apps/workforce_planning
```

**Nəticə:** Bütün app-lar həm host, həm konteynerdə mövcuddur. Volume mapping problemi YOXDUR. **ƏVVƏLKİ HESABATIN "fayllar yaradılmayıb" ehtimalı YANLIŞDIR.**

## Addım 1.2 — INSTALLED_APPS yoxlaması: HAMISI QEYDİYYATDADIR

**Mənbə:** `config/settings.py:62-121` (lokal app-lar, 30 ədəd):

```python
# Local apps (config/settings.py:90-120)
'apps.core', 'apps.workflow_engine', 'apps.approval_engine', 'apps.access_control',
'apps.policy_engine', 'apps.feature_flags', 'apps.accounts', 'apps.departments',
'apps.evaluations', 'apps.performance_reviews', 'apps.notifications', 'apps.reports',
'apps.development_plans', 'apps.audit', 'apps.sentiment_analysis', 'apps.support',
'apps.competencies', 'apps.training', 'apps.search', 'apps.workforce_planning',
'apps.continuous_feedback', 'apps.compensation', 'apps.leave_attendance',
'apps.recruitment', 'apps.dashboard', 'apps.onboarding', 'apps.wellness',
'apps.engagement', 'apps.system_settings', 'apps.superuser_tools',
```

**Əmr:** hər yeni app üçün konteynerdə `import` testi:

```
$ for a in ...; do docker compose exec -T web python -c "import apps.$a; print('OK')"; done
system_settings     : OK
superuser_tools     : OK
workflow_engine     : OK
approval_engine     : OK
access_control      : OK
policy_engine       : OK
feature_flags       : OK
support             : OK
engagement          : OK
wellness            : OK
sentiment_analysis  : OK
```

**Nəticə:** INSTALLED_APPS kök səbəb DEYİL — hamısı qeydiyyatlı və import olunur. (`apps.security` bilərəkdən INSTALLED_APPS-da deyil, yalnız middleware.)

## Addım 1.3 — URL qeydiyyatı yoxlaması

**Mənbə:** `config/urls.py:130-166` — bütün include-lar mövcuddur. **Kritik tapıntı:** engine app-ları iki yerdə include olunub, UI səhifələri səhv prefiksdə:

```python
# config/urls.py:145-149 — YALNIZ ui_urls (hər app-da tək dashboard/ səhifəsi)
path('workflow/', include('apps.workflow_engine.ui_urls', namespace='workflow_engine_ui')),
path('approval/', include('apps.approval_engine.ui_urls', namespace='approval_engine_ui')),
path('access-control/', include('apps.access_control.ui_urls', namespace='access_control_ui')),
path('policy-engine/', include('apps.policy_engine.ui_urls', namespace='policy_engine_ui')),
path('feature-flags/', include('apps.feature_flags.ui_urls', namespace='feature_flags_ui')),
```

```python
# config/api_urls.py:366-370 — Batch 14-18 UI səhifələri (workflows/, roles/, ...) SƏHVƏN BURADA
path('workflow/', include('apps.workflow_engine.urls')),      # → /api/v1/workflow/workflows/ ...
path('approval/', include('apps.approval_engine.urls')),
path('access-control/', include('apps.access_control.urls')), # → /api/v1/access-control/roles/ ...
path('policy-engine/', include('apps.policy_engine.urls')),
path('feature-flags/', include('apps.feature_flags.urls')),
```

Nümunə — `apps/access_control/urls.py` (UI + router qarışıq, `/api/v1/` altında yüklənir):

```python
urlpatterns = [
    path('roles/', views_extras.access_roles, name='roles'),
    path('permissions/', views_extras.access_permissions, name='permissions'),
    path('policies/', views_extras.access_policies, name='policies'),
    path('groups/', views_extras.access_groups, name='groups'),
    path('requests/', views_extras.access_requests, name='requests'),      # plan: access-requests
    path('history/', views_extras.access_history, name='history'),          # plan: access-history
    path('api/', include(router.urls)),
]
```

**Əmr:** resolver gəzintisi ilə qeydiyyatlı bütün URL sayı (`verify_161.py` içindəki `get_resolver()` gəzintisi):

```
REGCOUNT|2838
```

**Nəticə:** 2838 URL pattern qeydiyyatlıdır. Batch 14–18 səhifələri MÖVCUDDUR, lakin `/workflow/roles/` deyil, `/api/v1/workflow/...` altındadır. Bu, planlaşdırılan yollarda 404-ün əsas kök səbəbidir (FAZA 2.1/2.2 ALT testi ilə təsdiqləndi).

## Addım 1.4 — Migrasiya vəziyyəti: HAMISI TƏTBİQ OLUNUB

**Əmr:** `docker compose exec web python manage.py showmigrations` — yeni app-lar (tam çıxış blokları):

```
access_control
 [X] 0001_initial
 [X] 0002_alter_abacpolicy_options_alter_permission_options_and_more
 [X] 0003_accesshistory_accessrequest_usergroup
approval_engine
 [X] 0001_initial
 [X] 0002_alter_approvalchain_options_and_more
 [X] 0003_approvalrule
workflow_engine
 [X] 0001_initial
 [X] 0002_alter_workflowcondition_options_and_more
 [X] 0003_workflowlog_workflowversion
policy_engine
 [X] 0001_initial
 [X] 0002_alter_policy_options_alter_policyversion_options_and_more
 [X] 0003_policylog_policyrule
feature_flags
 [X] 0001_initial
 [X] 0002_alter_featureflag_options_and_more
 [X] 0003_environment_experiment_featureflaglog_and_more
system_settings
 [X] 0001_initial
superuser_tools
 (no migrations)
support
 [X] 0001_initial
 [X] 0002_slapolicy_ticketcategory_knowledgearticle
engagement
 [X] 0001_initial
 [X] 0002_engagementactionplan
wellness
 [X] 0001_initial
 [X] 0002_benefit_healthgoal_vaccinationrecord
sentiment_analysis
 [X] 0001_initial
```

Tam siyahının yekunu: **154 migrasiya `[X]` (tətbiq olunub), 0 ədəd `[ ]` (gözləyən)**. (Tam 189 sətirlik `showmigrations --list` çıxışı Addım 2.4-dədir.)

**Nəticə:** Migrasiya kök səbəb DEYİL. `superuser_tools`-da model olmadığı üçün migrasiya yoxdur — gözlənilən.

## Addım 1.5 — Konteyner vəziyyəti: SAĞLAM

**Əmr:** `docker compose ps` (tam çıxış):

```
NAME               IMAGE                      SERVICE       STATUS                      PORTS
q360_celery        q360_project-celery        celery        Up (healthy)                8000/tcp
q360_celery_beat   q360_project-celery-beat   celery-beat   Up (unhealthy)              8000/tcp
q360_db            postgres:16-alpine         db            Up (healthy)                0.0.0.0:5432->5432/tcp
q360_nginx         nginx:alpine               nginx         Up (unhealthy)              0.0.0.0:80->80, 443->443
q360_ngrok         ngrok/ngrok:latest         ngrok         Up                          0.0.0.0:4040->4040/tcp
q360_redis         redis:7-alpine             redis         Up (healthy)                6379/tcp
q360_web           q360_project-web           web           Up (healthy)                0.0.0.0:8000->8000/tcp
```

**Əmr:** `docker compose config` (web volume mount-ları — bind mapping təsdiqi):

```
web volumes:
  bind: host .../q360_project/apps   → /app/apps
  bind: host .../q360_project/config → /app/config
  bind: host .../q360_project        → /app
  volume: static_volume → /app/staticfiles, media_volume → /app/media
```

**Nəticə:** `web` konteyneri "healthy", 8000 portunda cavab verir. Kod host-dan `/app`-a bind olunub (köhnə image problemi yoxdur). `nginx`/`celery-beat` "unhealthy"-dir (healthcheck), amma bu 161 URL-ə aid deyil — Django birbaşa `web:8000`-də test olunur. **Konteyner kök səbəb DEYİL.**

## Addım 1.6 — Server xətaları: BAŞLANĞICDA XƏTA YOXDUR

**Əmr:** `docker compose logs web --tail=200 | grep -iE "error|traceback|exception"`

```
(grep exit: 1 — heç bir uyğunluq yoxdur, 0 nəticə)
```

Loglarda yalnız `GET /health/ 200` sətirlərı var. Server import/migration xətası olmadan başlayır:

```
q360_web | 127.0.0.1 - - [14/Jul/2026:15:02:56] "GET /health/" 200 35
```

**Nəticə:** Başlanğıcda xəta yoxdur. 500-lük xətalar yalnız konkret səhifələr açılarkən baş verir (FAZA 2.2).

## Addım 1.7 — Git vəziyyəti: HAMISI COMMIT EDİLİB

**Əmr:** `git status`

```
On branch master
Your branch is up to date with 'origin/master'.
nothing to commit, working tree clean
```
(Bu hesabat yaradılmazdan əvvəlki vəziyyət; indi yalnız `kritik_dogrulama_hesabati.md` untracked.)

**Əmr:** `git log --oneline -30` (161 səhifəyə aid batch commit-ləri):

```
26f3a93 feat(superuser): implement Batch 28 Superuser Tools
ff02d9f feat(support): implement Batch 27 Support additions
c7b3d60 feat(engagement): implement Batch 26 Engagement additions
4e379dc feat(wellness): implement Batch 25 Wellness additions
9f523c4 feat(sentiment): implement Batch 24 Sentiment additions
815995e feat(recruitment): implement Batch 23 Recruitment additions
afed978 feat(okr): implement Batch 22 OKR additions
6bed4dd feat(leave_attendance): implement Batch 21 Leave additions
6c2d187 feat(compensation): implement Batch 20 Compensation additions
8fef866 feat(accounts/pfile): implement Batch 19 P-File additions
a6f4cae feat(feature_flags): implement Batch 18 additions
705f10e feat(policy_engine): implement Batch 17 additions
abdc5fc feat(access_control): implement Batch 16 additions
52eae82 feat(approval_engine): implement Batch 15 additions
2e1dac6 feat(workflow_engine): implement Batch 14 additions
e338d2c feat(continuous_feedback): implement Batch 13 additions
d5a9139 feat(workforce_planning): implement Batch 12 additions
eb1f383 feat(audit): implement Batch 11 additions
eea7674 feat(training): implement Batch 10 additions
f68dff6 feat(competencies): implement Batch 9 additions
92c102f feat(notifications): implement Batch 8 additions
b8af06b feat(development_plans): implement Batch 7 additions
5f2cffe feat(reports): implement Batch 6 additions
5d10410 feat(departments): implement Batch 5 additions
d38ab4d feat(evaluations): implement Batch 4 additions
1de0cb0 feat(dashboard): implement Batch 3 additions
0cb7abc feat(settings): verify and audit Batch 1 and Batch 2 implementation
```

**Nəticə:** Kod push edilib, hər batch ayrıca commit-dədir. Fayllar "lokal qalıb" və ya "yaradılmayıb" DEYİL.

### FAZA 1 XÜLASƏSİ — kök səbəb

Fayllar var (1.1), INSTALLED_APPS tam (1.2), migrasiyalar tətbiq olunub (1.4), konteyner sağlam (1.5), başlanğıc xətası yoxdur (1.6), kod commit edilib (1.7). Buraxılmış addım **URL routing və view kodudur** (1.3 + FAZA 2): (a) Batch 14–18 UI-ları səhv prefiksdə (`/api/v1/`), (b) Batch 19 import xətası, (c) Batch 22/23/26/27 ORM sahə xətaları, (d) Batch 3/4/8 heç yaradılmamış yollar.

---

# FAZA 2 — TAM DOĞRULAMA

## Addım 2.1 — URL-BY-URL MÜQAYİSƏ (CLAUDE.md-də göstərilən 4 uyğunsuzluq)

| Uyğunsuzluq | Faktiki nəticə (əmr çıxışına əsasən) |
|-------------|--------------------------------------|
| **Batch 3:** `/dashboard/export/` itibmi? | Bəli. `T\|3\|/dashboard/export/\|404`. Yalnız `/dashboard/export/analytics/excel/`, `/export/analytics/pdf/`, `/export-model/` var (`apps/dashboard/urls.py:22-30`) — onlar da FieldError/500 verir. |
| **Batch 4:** `forms/`, `calibration/`, `weights/` niyə yoxdur? | `forms/`+`weights/` heç yaradılmayıb (`404`). `calibration/` `campaign_id` tələb edir: `T\|4\|/evaluations/calibration/\|404`, amma `ALT\|/evaluations/calibration/1/\|200` (`apps/evaluations/urls.py:61`). |
| **Batch 13:** `/feedback/` vs `/continuous-feedback/` | Ziddiyyət yoxdur. `continuous_feedback` app `/feedback/` prefiksinə bağlıdır (`config/urls.py:141`). `T\|13\|/feedback/templates/\|200`. ✅ |
| **Batch 16:** `access-requests`vs`requests`, `access-history`vs`history` | Adlandırma fərqi TƏSDİQLƏNDİ. Plan `access-requests/`/`access-history/`, kod `requests/`/`history/` (`apps/access_control/urls.py`). Üstəlik `/api/v1/access-control/` altında: `ALT\|/api/v1/access-control/requests/\|200`, `ALT\|/api/v1/access-control/history/\|200`. Planlaşdırılan hər iki forma = 404. |

**ALT test — 404 alan planlaşdırılan yolların faktiki nüsxələri (tam əmr çıxışı, `verify_alt.py`):**

```
ALT|/dashboard/export/|/dashboard/export/analytics/excel/|EXC|FieldError: Cannot resolve keyword 'status'...
ALT|/dashboard/export/|/dashboard/export-model/|EXC|FieldError: Cannot resolve keyword 'metric_name'...
ALT|/evaluations/calibration/|/evaluations/calibration/1/|200|
ALT|/notifications/email-templates/|/notifications/templates/emails/|200|
ALT|/notifications/sms-templates/|/notifications/templates/sms/|200|
ALT|/notifications/push-templates/|/notifications/templates/push/|200|
ALT|/workflow/workflows/|/api/v1/workflow/workflows/|EXC|NoReverseMatch: 'workflow_engine' is not a registered namespace
ALT|/workflow/designer/|/api/v1/workflow/designer/|200|
ALT|/workflow/versions/|/api/v1/workflow/versions/|200|
ALT|/workflow/history/|/api/v1/workflow/history/|200|
ALT|/workflow/logs/|/api/v1/workflow/logs/|200|
ALT|/workflow/monitoring/|/api/v1/workflow/monitoring/|200|
ALT|/approval/rules/|/api/v1/approval/rules/|200|
ALT|/approval/chains/|/api/v1/approval/chains/|200|
ALT|/approval/history/|/api/v1/approval/history/|200|
ALT|/approval/queue/|/api/v1/approval/queue/|200|
ALT|/approval/delegations/|/api/v1/approval/delegations/|200|
ALT|/access-control/roles/|/api/v1/access-control/roles/|200|
ALT|/access-control/permissions/|/api/v1/access-control/permissions/|200|
ALT|/access-control/policies/|/api/v1/access-control/policies/|200|
ALT|/access-control/groups/|/api/v1/access-control/groups/|200|
ALT|/access-control/access-requests/|/api/v1/access-control/requests/|200|
ALT|/access-control/access-history/|/api/v1/access-control/history/|200|
ALT|/policy-engine/policies/|/api/v1/policy-engine/policies/|200|
ALT|/policy-engine/rules/|/api/v1/policy-engine/rules/|200|
ALT|/policy-engine/simulator/|/api/v1/policy-engine/simulator/|200|
ALT|/policy-engine/versions/|/api/v1/policy-engine/versions/|200|
ALT|/policy-engine/logs/|/api/v1/policy-engine/logs/|200|
ALT|/feature-flags/flags/|/api/v1/feature-flags/flags/|200|
ALT|/feature-flags/environments/|/api/v1/feature-flags/environments/|200|
ALT|/feature-flags/rollouts/|/api/v1/feature-flags/rollouts/|200|
ALT|/feature-flags/experiments/|/api/v1/feature-flags/experiments/|200|
ALT|/feature-flags/history/|/api/v1/feature-flags/history/|200|
ALT|/support/tickets/{id}/|/support/1/|EXC|FieldError: select_related: 'user'. Choices are: ticket, created_by
```

## Addım 2.2 — TEST CLIENT İLƏ STATUS: 161 URL VAHİD MASTER CƏDVƏLİ

Superuser `admin` ilə `force_login`, hər URL GET. `Qeyd.da` = planlaşdırılan yolun resolver-də qeydiyyatı (var/yox). Status `500` = test client-də exception (DEBUG=True; production-da HTTP 500).

**Xam əmr çıxışının yekunu:**
```
=== T statusları ===  117×200,  35×404,  9×EXC(=500)
```

| # | B | Plan URL | Faktiki test URL | Qeyd.da | Status | Qeyd |
|---|---|----------|------------------|---------|--------|------|
| 1 | 1 | `/settings/` | `/settings/` | var | 200 |  |
| 2 | 1 | `/settings/general/` | `/settings/general/` | var | 200 |  |
| 3 | 1 | `/settings/localization/` | `/settings/localization/` | var | 200 |  |
| 4 | 1 | `/settings/languages/` | `/settings/languages/` | var | 200 |  |
| 5 | 1 | `/settings/timezone/` | `/settings/timezone/` | var | 200 |  |
| 6 | 1 | `/settings/currency/` | `/settings/currency/` | var | 200 |  |
| 7 | 1 | `/settings/branding/` | `/settings/branding/` | var | 200 |  |
| 8 | 1 | `/settings/company/` | `/settings/company/` | var | 200 |  |
| 9 | 1 | `/settings/security/` | `/settings/security/` | var | 200 |  |
| 10 | 1 | `/settings/authentication/` | `/settings/authentication/` | var | 200 |  |
| 11 | 1 | `/settings/password-policy/` | `/settings/password-policy/` | var | 200 |  |
| 12 | 1 | `/settings/integrations/` | `/settings/integrations/` | var | 200 |  |
| 13 | 1 | `/settings/api/` | `/settings/api/` | var | 200 |  |
| 14 | 1 | `/settings/api-keys/` | `/settings/api-keys/` | var | 200 |  |
| 15 | 1 | `/settings/webhooks/` | `/settings/webhooks/` | var | 200 |  |
| 16 | 1 | `/settings/email/` | `/settings/email/` | var | 200 |  |
| 17 | 1 | `/settings/sms/` | `/settings/sms/` | var | 200 |  |
| 18 | 1 | `/settings/storage/` | `/settings/storage/` | var | 200 |  |
| 19 | 1 | `/settings/backups/` | `/settings/backups/` | var | 200 |  |
| 20 | 1 | `/settings/audit/` | `/settings/audit/` | var | 200 |  |
| 21 | 1 | `/settings/licenses/` | `/settings/licenses/` | var | 200 |  |
| 22 | 1 | `/settings/system/` | `/settings/system/` | var | 200 |  |
| 23 | 1 | `/settings/mfa/` | `/settings/mfa/` | var | 200 | STUB "Tezliklə" |
| 24 | 1 | `/settings/sso/` | `/settings/sso/` | var | 200 | STUB "Tezliklə" |
| 25 | 2 | `/accounts/sessions/` | `/accounts/sessions/` | var | 200 |  |
| 26 | 2 | `/accounts/devices/` | `/accounts/devices/` | var | 200 |  |
| 27 | 2 | `/accounts/activity/` | `/accounts/activity/` | var | 200 |  |
| 28 | 2 | `/accounts/api-tokens/` | `/accounts/api-tokens/` | var | 200 |  |
| 29 | 2 | `/accounts/preferences/` | `/accounts/preferences/` | var | 200 |  |
| 30 | 2 | `/accounts/preferences/appearance/` | `/accounts/preferences/appearance/` | var | 200 |  |
| 31 | 2 | `/accounts/preferences/notifications/` | `/accounts/preferences/notifications/` | var | 200 |  |
| 32 | 3 | `/dashboard/widgets/` | `/dashboard/widgets/` | var | 200 |  |
| 33 | 3 | `/dashboard/settings/` | `/dashboard/settings/` | var | 200 |  |
| 34 | 3 | `/dashboard/export/` | `/dashboard/export/` | yox | 404 | Alt /export/analytics/excel/ = 500(FieldError) |
| 35 | 3 | `/dashboard/favorites/` | `/dashboard/favorites/` | var | 200 |  |
| 36 | 4 | `/evaluations/templates/` | `/evaluations/templates/` | var | 200 |  |
| 37 | 4 | `/evaluations/forms/` | `/evaluations/forms/` | yox | 404 | Yaradılmayıb |
| 38 | 4 | `/evaluations/calibration/` | `/evaluations/calibration/` | yox | 404 | Faktiki: /evaluations/calibration/1/ = 200 |
| 39 | 4 | `/evaluations/review-cycles/` | `/evaluations/review-cycles/` | var | 200 |  |
| 40 | 4 | `/evaluations/history/` | `/evaluations/history/` | var | 200 |  |
| 41 | 4 | `/evaluations/settings/` | `/evaluations/settings/` | var | 200 |  |
| 42 | 4 | `/evaluations/weights/` | `/evaluations/weights/` | yox | 404 | Yaradılmayıb |
| 43 | 5 | `/departments/positions/` | `/departments/positions/` | var | 200 |  |
| 44 | 5 | `/departments/job-titles/` | `/departments/job-titles/` | var | 200 |  |
| 45 | 5 | `/departments/history/` | `/departments/history/` | var | 200 |  |
| 46 | 6 | `/reports/saved/` | `/reports/saved/` | var | 200 |  |
| 47 | 6 | `/reports/export/` | `/reports/export/` | var | 200 |  |
| 48 | 6 | `/reports/history/` | `/reports/history/` | var | 200 |  |
| 49 | 6 | `/reports/data-warehouse/` | `/reports/data-warehouse/` | var | 200 |  |
| 50 | 7 | `/development-plans/progress/` | `/development-plans/progress/` | var | 200 |  |
| 51 | 7 | `/development-plans/roadmap/` | `/development-plans/roadmap/` | var | 200 |  |
| 52 | 7 | `/development-plans/approvals/` | `/development-plans/approvals/` | var | 200 |  |
| 53 | 8 | `/notifications/email-templates/` | `/notifications/email-templates/` | yox | 404 | Faktiki: /notifications/templates/emails/ = 200 |
| 54 | 8 | `/notifications/sms-templates/` | `/notifications/sms-templates/` | yox | 404 | Faktiki: /notifications/templates/sms/ = 200 |
| 55 | 8 | `/notifications/push-templates/` | `/notifications/push-templates/` | yox | 404 | Faktiki: /notifications/templates/push/ = 200 |
| 56 | 8 | `/notifications/webhooks/` | `/notifications/webhooks/` | var | 200 |  |
| 57 | 8 | `/notifications/delivery-logs/` | `/notifications/delivery-logs/` | var | 200 |  |
| 58 | 8 | `/notifications/queue/` | `/notifications/queue/` | var | 200 |  |
| 59 | 9 | `/competencies/dictionary/` | `/competencies/dictionary/` | var | 200 |  |
| 60 | 9 | `/competencies/rating-scales/` | `/competencies/rating-scales/` | var | 200 |  |
| 61 | 9 | `/competencies/behaviors/` | `/competencies/behaviors/` | var | 200 |  |
| 62 | 10 | `/training/courses/` | `/training/courses/` | var | 200 |  |
| 63 | 10 | `/training/learning-paths/` | `/training/learning-paths/` | var | 200 |  |
| 64 | 10 | `/training/course-categories/` | `/training/course-categories/` | var | 200 |  |
| 65 | 10 | `/training/exams/` | `/training/exams/` | var | 200 |  |
| 66 | 11 | `/audit/events/` | `/audit/events/` | var | 200 |  |
| 67 | 11 | `/audit/login-history/` | `/audit/login-history/` | var | 200 |  |
| 68 | 11 | `/audit/user-history/` | `/audit/user-history/` | var | 200 |  |
| 69 | 11 | `/audit/api/` | `/audit/api/` | var | 200 |  |
| 70 | 11 | `/audit/security-incidents/` | `/audit/security-incidents/` | var | 200 |  |
| 71 | 11 | `/audit/export/` | `/audit/export/` | var | 200 |  |
| 72 | 12 | `/workforce-planning/risk-heatmap/` | `/workforce-planning/risk-heatmap/` | var | 200 |  |
| 73 | 12 | `/workforce-planning/retirement-forecast/` | `/workforce-planning/retirement-forecast/` | var | 200 |  |
| 74 | 13 | `/feedback/templates/` | `/feedback/templates/` | var | 200 |  |
| 75 | 13 | `/feedback/requests/` | `/feedback/requests/` | var | 200 |  |
| 76 | 13 | `/feedback/reminders/` | `/feedback/reminders/` | var | 200 |  |
| 77 | 14 | `/workflow/workflows/` | `/workflow/workflows/` | yox | 404 | Alt /api/v1/workflow/workflows/ = 500(NoReverseMatch) |
| 78 | 14 | `/workflow/designer/` | `/workflow/designer/` | yox | 404 | Faktiki: /api/v1/workflow/designer/ = 200 (STUB) |
| 79 | 14 | `/workflow/versions/` | `/workflow/versions/` | yox | 404 | Faktiki: /api/v1/workflow/versions/ = 200 |
| 80 | 14 | `/workflow/history/` | `/workflow/history/` | yox | 404 | Faktiki: /api/v1/workflow/history/ = 200 |
| 81 | 14 | `/workflow/logs/` | `/workflow/logs/` | yox | 404 | Faktiki: /api/v1/workflow/logs/ = 200 |
| 82 | 14 | `/workflow/monitoring/` | `/workflow/monitoring/` | yox | 404 | Faktiki: /api/v1/workflow/monitoring/ = 200 |
| 83 | 15 | `/approval/rules/` | `/approval/rules/` | yox | 404 | Faktiki: /api/v1/approval/rules/ = 200 |
| 84 | 15 | `/approval/chains/` | `/approval/chains/` | yox | 404 | Faktiki: /api/v1/approval/chains/ = 200 |
| 85 | 15 | `/approval/history/` | `/approval/history/` | yox | 404 | Faktiki: /api/v1/approval/history/ = 200 |
| 86 | 15 | `/approval/queue/` | `/approval/queue/` | yox | 404 | Faktiki: /api/v1/approval/queue/ = 200 |
| 87 | 15 | `/approval/delegations/` | `/approval/delegations/` | yox | 404 | Faktiki: /api/v1/approval/delegations/ = 200 |
| 88 | 16 | `/access-control/roles/` | `/access-control/roles/` | yox | 404 | 🔴 Faktiki: /api/v1/access-control/roles/ = 200 (adi user açır) |
| 89 | 16 | `/access-control/permissions/` | `/access-control/permissions/` | yox | 404 | 🔴 Faktiki: /api/v1/access-control/permissions/ = 200 |
| 90 | 16 | `/access-control/policies/` | `/access-control/policies/` | yox | 404 | 🔴 Faktiki: /api/v1/access-control/policies/ = 200 |
| 91 | 16 | `/access-control/groups/` | `/access-control/groups/` | yox | 404 | 🔴 Faktiki: /api/v1/access-control/groups/ = 200 |
| 92 | 16 | `/access-control/access-requests/` | `/access-control/access-requests/` | yox | 404 | 🔴 Faktiki: /api/v1/access-control/requests/ = 200 |
| 93 | 16 | `/access-control/access-history/` | `/access-control/access-history/` | yox | 404 | 🔴 Faktiki: /api/v1/access-control/history/ = 200 |
| 94 | 17 | `/policy-engine/policies/` | `/policy-engine/policies/` | yox | 404 | 🔴 Faktiki: /api/v1/policy-engine/policies/ = 200 |
| 95 | 17 | `/policy-engine/rules/` | `/policy-engine/rules/` | yox | 404 | 🔴 Faktiki: /api/v1/policy-engine/rules/ = 200 |
| 96 | 17 | `/policy-engine/simulator/` | `/policy-engine/simulator/` | yox | 404 | 🔴 Faktiki: /api/v1/policy-engine/simulator/ = 200 (STUB) |
| 97 | 17 | `/policy-engine/versions/` | `/policy-engine/versions/` | yox | 404 | 🔴 Faktiki: /api/v1/policy-engine/versions/ = 200 |
| 98 | 17 | `/policy-engine/logs/` | `/policy-engine/logs/` | yox | 404 | 🔴 Faktiki: /api/v1/policy-engine/logs/ = 200 |
| 99 | 18 | `/feature-flags/flags/` | `/feature-flags/flags/` | yox | 404 | Faktiki: /api/v1/feature-flags/flags/ = 200 |
| 100 | 18 | `/feature-flags/environments/` | `/feature-flags/environments/` | yox | 404 | Faktiki: /api/v1/feature-flags/environments/ = 200 |
| 101 | 18 | `/feature-flags/rollouts/` | `/feature-flags/rollouts/` | yox | 404 | Faktiki: /api/v1/feature-flags/rollouts/ = 200 |
| 102 | 18 | `/feature-flags/experiments/` | `/feature-flags/experiments/` | yox | 404 | Faktiki: /api/v1/feature-flags/experiments/ = 200 |
| 103 | 18 | `/feature-flags/history/` | `/feature-flags/history/` | yox | 404 | Faktiki: /api/v1/feature-flags/history/ = 200 |
| 104 | 19 | `/pfile/employees/create/` | `/pfile/employees/create/` | var | 500 | NameError: '_' is not defined |
| 105 | 19 | `/pfile/employees/import/` | `/pfile/employees/import/` | var | 500 | NameError: '_' is not defined |
| 106 | 19 | `/pfile/documents/` | `/pfile/documents/` | var | 500 | NameError: '_' is not defined |
| 107 | 19 | `/pfile/contracts/` | `/pfile/contracts/` | var | 500 | NameError: '_' is not defined |
| 108 | 19 | `/pfile/assets/` | `/pfile/assets/` | var | 500 | NameError: '_' is not defined |
| 109 | 19 | `/pfile/emergency-contacts/` | `/pfile/emergency-contacts/` | var | 500 | NameError: '_' is not defined |
| 110 | 20 | `/compensation/pay-grades/` | `/compensation/pay-grades/` | var | 200 |  |
| 111 | 20 | `/compensation/salary-bands/` | `/compensation/salary-bands/` | var | 200 |  |
| 112 | 20 | `/compensation/currencies/` | `/compensation/currencies/` | var | 200 |  |
| 113 | 20 | `/compensation/cycles/` | `/compensation/cycles/` | var | 200 |  |
| 114 | 21 | `/leave/types/` | `/leave/types/` | var | 200 |  |
| 115 | 21 | `/leave/holidays/` | `/leave/holidays/` | var | 200 |  |
| 116 | 21 | `/leave/balances/` | `/leave/balances/` | var | 200 |  |
| 117 | 21 | `/leave/carry-over/` | `/leave/carry-over/` | var | 200 |  |
| 118 | 21 | `/leave/settings/` | `/leave/settings/` | var | 200 |  |
| 119 | 22 | `/okr/key-results/` | `/okr/key-results/` | var | 200 |  |
| 120 | 22 | `/okr/initiatives/` | `/okr/initiatives/` | var | 200 |  |
| 121 | 22 | `/okr/check-ins/` | `/okr/check-ins/` | var | 500 | FieldError: select_related('user') → düzgün: created_by |
| 122 | 22 | `/okr/templates/` | `/okr/templates/` | var | 200 |  |
| 123 | 23 | `/recruitment/candidates/` | `/recruitment/candidates/` | var | 200 |  |
| 124 | 23 | `/recruitment/offers/` | `/recruitment/offers/` | var | 200 |  |
| 125 | 23 | `/recruitment/talent-pool/` | `/recruitment/talent-pool/` | var | 200 |  |
| 126 | 23 | `/recruitment/referrals/` | `/recruitment/referrals/` | var | 500 | FieldError: select_related('referred_by') → düzgün: referrer |
| 127 | 23 | `/recruitment/interview-feedback/` | `/recruitment/interview-feedback/` | var | 200 |  |
| 128 | 24 | `/sentiment/reports/` | `/sentiment-analysis/reports/` | var | 200 | STUB "Tezliklə" |
| 129 | 24 | `/sentiment/history/` | `/sentiment-analysis/history/` | var | 200 | Marker YOX |
| 130 | 24 | `/sentiment/trends/` | `/sentiment-analysis/trends/` | var | 200 | STUB "Tezliklə" |
| 131 | 25 | `/wellness/benefits/` | `/wellness/benefits/` | var | 200 |  |
| 132 | 25 | `/wellness/health-goals/` | `/wellness/health-goals/` | var | 200 |  |
| 133 | 25 | `/wellness/vaccinations/` | `/wellness/vaccinations/` | var | 200 |  |
| 134 | 26 | `/engagement/analytics/` | `/engagement/analytics/` | var | 200 |  |
| 135 | 26 | `/engagement/anonymous-feedback/` | `/engagement/anonymous-feedback/` | var | 500 | FieldError: 'created_at' sahəsi yoxdur (responded_at var) |
| 136 | 26 | `/engagement/action-plans/` | `/engagement/action-plans/` | var | 200 |  |
| 137 | 27 | `/support/tickets/` | `/support/tickets/` | var | 200 |  |
| 138 | 27 | `/support/tickets/{id}/` | `/support/tickets/1/` | yox | 404 | Detail yolu yox; /support/1/ = 500(FieldError select_related('user')) |
| 139 | 27 | `/support/knowledge-base/` | `/support/knowledge-base/` | var | 200 |  |
| 140 | 27 | `/support/categories/` | `/support/categories/` | var | 200 |  |
| 141 | 27 | `/support/sla/` | `/support/sla/` | var | 200 |  |
| 142 | 27 | `/support/history/` | `/support/history/` | var | 200 |  |
| 143 | 28 | `/files/` | `/files/` | var | 200 | STUB "tezliklə" |
| 144 | 28 | `/files/uploads/` | `/files/uploads/` | var | 200 | STUB |
| 145 | 28 | `/files/library/` | `/files/library/` | var | 200 | STUB |
| 146 | 28 | `/imports/` | `/imports/` | var | 200 | STUB |
| 147 | 28 | `/exports/` | `/exports/` | var | 200 | STUB |
| 148 | 28 | `/ai/` | `/ai/` | var | 200 | STUB |
| 149 | 28 | `/ai/prompts/` | `/ai/prompts/` | var | 200 | STUB |
| 150 | 28 | `/ai/models/` | `/ai/models/` | var | 200 | STUB |
| 151 | 28 | `/ai/history/` | `/ai/history/` | var | 200 | STUB |
| 152 | 28 | `/system/` | `/system/` | var | 200 | STUB |
| 153 | 28 | `/system/health/` | `/system/health/` | var | 200 | STUB |
| 154 | 28 | `/system/status/` | `/system/status/` | var | 200 | STUB |
| 155 | 28 | `/system/jobs/` | `/system/jobs/` | var | 200 | STUB |
| 156 | 28 | `/system/cache/` | `/system/cache/` | var | 200 | STUB |
| 157 | 28 | `/system/queues/` | `/system/queues/` | var | 200 | STUB |
| 158 | 28 | `/admin/` | `/admin-panel/` | var | 200 | STUB; plan /admin/ (Django admin) → faktiki /admin-panel/ |
| 159 | 28 | `/admin/jobs/` | `/admin-panel/jobs/` | var | 200 | STUB |
| 160 | 28 | `/admin/maintenance/` | `/admin-panel/maintenance/` | var | 200 | STUB |
| 161 | 28 | `/admin/feature-toggles/` | `/admin-panel/feature-toggles/` | var | 200 | STUB |

## Addım 2.3 — Təhlükəsizlik testi

Tam nəticə və əmr çıxışları **Bölmə 0**-dadır (hesabatın başı). Xülasə: superuser-only Batch 28/Settings düzgün qorunur (302; 0×200 adi istifadəçi); LAKİN Batch 14–18 idarəetmə UI-ları `/api/v1/` altında yalnız `@login_required` ilə — adi istifadəçiyə 26×200 (🔴 KRİTİK).

## Addım 2.4 — `manage.py check` və `showmigrations --list` (tam çıxış)

**Əmr:** `docker compose exec web python manage.py check`

```
System check identified no issues (0 silenced).
[exit=0]
```

**Əmr:** `docker compose exec web python manage.py showmigrations --list` (tam, kəsilməmiş):

```
access_control
 [X] 0001_initial
 [X] 0002_alter_abacpolicy_options_alter_permission_options_and_more
 [X] 0003_accesshistory_accessrequest_usergroup
accounts
 [X] 0001_initial
 [X] 0002_initial
 [X] 0003_historicalprofile_city_and_more
 [X] 0004_alter_user_managers
 [X] 0005_usermfaconfig
 [X] 0006_historicalprofile_two_factor_backup_codes_and_more
 [X] 0007_alter_historicaluser_role_alter_user_role_apitoken_and_more
 [X] 0008_asset_contract_emergencycontact
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
 [X] 0003_logentry_add_action_flag_choices
approval_engine
 [X] 0001_initial
 [X] 0002_alter_approvalchain_options_and_more
 [X] 0003_approvalrule
audit
 [X] 0001_initial
 [X] 0002_alter_auditlog_action
 [X] 0003_auditlog_actor_role_auditlog_context_and_more
 [X] 0004_auditlog_search_vector_auditlog_audit_search_idx
 [X] 0005_add_threat_fields
 [X] 0006_blockedip
 [X] 0007_apirequestlog_securityincident
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
 [X] 0003_alter_user_email_max_length
 [X] 0004_alter_user_username_opts
 [X] 0005_alter_user_last_login_null
 [X] 0006_require_contenttypes_0002
 [X] 0007_alter_validators_add_error_messages
 [X] 0008_alter_user_username_max_length
 [X] 0009_alter_user_last_name_max_length
 [X] 0010_alter_group_name_max_length
 [X] 0011_update_proxy_permissions
 [X] 0012_alter_user_first_name_max_length
compensation
 [X] 0001_initial
 [X] 0002_historicaldepartmentbudget_departmentbudget
 [X] 0003_alter_salaryinformation_user
 [X] 0004_historicalmarketbenchmark_historicalequitygrant_and_more
 [X] 0005_employeebenefit
 [X] 0006_currency_paygrade_payrollcycle_salaryband
competencies
 [X] 0001_initial
 [X] 0002_competency_competencie_name_eac81b_idx_and_more
 [X] 0003_behavioralindicator
contenttypes
 [X] 0001_initial
 [X] 0002_remove_content_type_name
continuous_feedback
 [X] 0001_initial
 [X] 0002_quickfeedback_anonymous_hash_and_more
 [X] 0003_alter_feedbackbank_average_rating_and_more
 [X] 0004_feedbacktemplate_feedbackreminder_feedbackrequest
dashboard
 [X] 0001_initial
 [X] 0002_dashboardsetting_favoriteitem_userdashboardwidget
departments
 [X] 0001_initial
 [X] 0002_remove_department_departments_department_tref4ab
 [X] 0003_remove_historicalposition_level
 [X] 0004_historicalposition_level
 [X] 0005_department_departments_department_tref4ab
 [X] 0006_remove_department_departments_department_tref4ab
 [X] 0007_department_departments_department_tref4ab
 [X] 0008_remove_department_departments_department_tref4ab
 [X] 0009_department_departments_department_tref4ab
 [X] 0010_remove_department_departments_department_tref4ab
 [X] 0011_department_departments_department_tref4ab
 [X] 0012_remove_department_departments_department_tref4ab
 [X] 0013_department_departments_department_tref4ab
 [X] 0014_remove_department_departments_department_tref4ab
 [X] 0015_jobtitle_historicaljobtitle
development_plans
 [X] 0001_initial
 [X] 0002_developmentgoal_approval_note_and_more
 [X] 0003_progresslog_is_draft_progresslog_updated_at
 [X] 0004_developmentgoal_is_approved
 [X] 0005_remove_is_approved_field
 [X] 0006_kpi_strategicobjective_kpimeasurement_kpi_objective_and_more
 [X] 0007_historicalmilestone_historicalobjectiveupdate_and_more
 [X] 0008_developmentgoal_alignment_percentage_and_more
 [X] 0009_initiative_okrtemplate
django_celery_beat
 [X] 0001_initial
 [X] 0002_auto_20161118_0346
 [X] 0003_auto_20161209_0049
 [X] 0004_auto_20170221_0000
 [X] 0005_add_solarschedule_events_choices
 [X] 0006_auto_20180322_0932
 [X] 0007_auto_20180521_0826
 [X] 0008_auto_20180914_1922
 [X] 0006_auto_20180210_1226
 [X] 0006_periodictask_priority
 [X] 0009_periodictask_headers
 [X] 0010_auto_20190429_0326
 [X] 0011_auto_20190508_0153
 [X] 0012_periodictask_expire_seconds
 [X] 0013_auto_20200609_0727
 [X] 0014_remove_clockedschedule_enabled
 [X] 0015_edit_solarschedule_events_choices
 [X] 0016_alter_crontabschedule_timezone
 [X] 0017_alter_crontabschedule_month_of_year
 [X] 0018_improve_crontab_helptext
 [X] 0019_alter_periodictasks_options
engagement
 [X] 0001_initial
 [X] 0002_engagementactionplan
evaluations
 [X] 0001_initial
 [X] 0002_update_score_validators_to_5
 [X] 0003_response_sentiment_category_response_sentiment_score
 [X] 0004_evaluationcampaign_evaluations_status_540c61_idx_and_more
 [X] 0005_evaluationcampaign_weight_peer_and_more
 [X] 0006_calibrationlog
 [X] 0007_evaluationsetting_reviewcycle_evaluationtemplate_and_more
feature_flags
 [X] 0001_initial
 [X] 0002_alter_featureflag_options_and_more
 [X] 0003_environment_experiment_featureflaglog_and_more
leave_attendance
 [X] 0001_initial
 [X] 0002_leavesettings
notifications
 [X] 0001_initial
 [X] 0002_emaillog
 [X] 0003_notificationmethod_smsprovider_notification_channel_and_more
 [X] 0004_smsnotification_pushnotification_priority_and_more
 [X] 0005_alter_smsprovider_provider
onboarding
 [X] 0001_initial
 [X] 0002_default_template
 [X] 0003_rename_onboarding_title_r_1e763a_idx_onboarding__title_f6c2b0_idx_and_more
 [X] 0004_alter_onboardingtask_task_type
 [X] 0005_alter_onboardingprocess_unique_together
 [X] 0006_onboardingnote
performance_reviews
 [X] 0001_initial
policy_engine
 [X] 0001_initial
 [X] 0002_alter_policy_options_alter_policyversion_options_and_more
 [X] 0003_policylog_policyrule
recruitment
 [X] 0001_initial
 [X] 0002_historicalreferral_historicalcandidateexperience_and_more
 [X] 0003_talentpool
reports
 [X] 0001_initial
 [X] 0002_add_report_generation_log
 [X] 0003_systemkpi
 [X] 0004_reportblueprint_reportschedule_reportvisualization_and_more
 [X] 0005_scheduledreport_reportschedule_delivery_emails_and_more
 [X] 0006_alter_reportschedule_additional_emails_and_more
 [X] 0007_alter_report_data_alter_report_generated_by
search
 [X] 0001_add_trigram_indexes
sentiment_analysis
 [X] 0001_initial
sessions
 [X] 0001_initial
superuser_tools
 (no migrations)
support
 [X] 0001_initial
 [X] 0002_slapolicy_ticketcategory_knowledgearticle
system_settings
 [X] 0001_initial
training
 [X] 0001_initial
 [X] 0002_trainingresource_training_tr_provide_516d62_idx_and_more
 [X] 0003_certification_historicalcertification_and_more
 [X] 0004_coursecategory_exam_learningpath
wellness
 [X] 0001_initial
 [X] 0002_benefit_healthgoal_vaccinationrecord
workflow_engine
 [X] 0001_initial
 [X] 0002_alter_workflowcondition_options_and_more
 [X] 0003_workflowlog_workflowversion
workforce_planning
 [X] 0001_initial
 [X] 0002_retirementforecast
```

Yekun: **154 × `[X]`, 0 × `[ ]`**. `superuser_tools` model yoxdur — migrasiya yoxdur (gözlənilən).

## Addım 2.5 — STUB səhifələrinin yoxlanışı (tam əmr çıxışı)

Test client cavabındakı HTML-də "Tezliklə/Hazırlanır/Coming soon/TODO" markeri axtarıldı; hər 200 səhifənin HTML-i scratchpad-a saxlanıldı. **Məhdudiyyət:** headless brauzer quraşdırılmayıb — "ekran görüntüsü" əvəzinə render olunmuş HTML mətni yoxlandı.

```
STUB|/settings/mfa/|200|Tezlikl
STUB|/settings/sso/|200|Tezlikl
STUB|/workflow/designer/|404|ACILMADI          (planlaşdırılan yolda 404; faktiki /api/v1/... = 200)
STUB|/policy-engine/simulator/|404|ACILMADI    (planlaşdırılan yolda 404; faktiki /api/v1/... = 200)
STUB|/sentiment-analysis/reports/|200|Tezlikl
STUB|/sentiment-analysis/history/|200|MARKER_YOX
STUB|/sentiment-analysis/trends/|200|Tezlikl
STUB|/files/|200|tezlikl
STUB|/files/uploads/|200|tezlikl
STUB|/files/library/|200|tezlikl
STUB|/imports/|200|tezlikl
STUB|/exports/|200|tezlikl
STUB|/ai/|200|tezlikl
STUB|/ai/prompts/|200|tezlikl
STUB|/ai/models/|200|tezlikl
STUB|/ai/history/|200|tezlikl
STUB|/system/|200|tezlikl
STUB|/system/health/|200|tezlikl
STUB|/system/status/|200|tezlikl
STUB|/system/jobs/|200|tezlikl
STUB|/system/cache/|200|tezlikl
STUB|/system/queues/|200|tezlikl
STUB|/admin-panel/|200|tezlikl
STUB|/admin-panel/jobs/|200|tezlikl
STUB|/admin-panel/maintenance/|200|tezlikl
STUB|/admin-panel/feature-toggles/|200|tezlikl
```

**Əmr:** `designer/` və `simulator/` faktiki (`/api/v1/...`) yolda marker yoxlaması:

```
STUB2|/api/v1/workflow/designer/|200|MARKER_YOX
STUB2|/api/v1/policy-engine/simulator/|200|MARKER_YOX
```

**Nəticə:** Batch 28 (19 səhifə) + MFA/SSO + Sentiment reports/trends düzgün "Tezliklə" göstərir. LAKİN `designer/` və `simulator/` STUB kimi nəzərdə tutulub (CLAUDE.md Batch 14/17), amma istifadəçiyə "Tezliklə" göstərmir — real funksionallıq kimi görünür. `/sentiment-analysis/history/` də markersizdir.

---

# BATCH-BATCH STATUS (əvvəlki hesabatın "✅ TAMAMLANDI" iddiasına qarşı)

Qayda: batch-in BÜTÜN URL-ləri planlaşdırılan yolda qeydiyyatda + auth ilə 200/302 → **TƏSDİQLƏNDİ**; hər hansı URL 404/500 → **TƏSDİQLƏNMƏDİ**.

| Batch | Əvvəlki iddia | Faktiki (əmr çıxışı) | Yeni status | Səbəb |
|-------|---------------|----------------------|-------------|-------|
| 1 — Settings (24) | ✅ TAMAMLANDI | 24/24 = 200 | **TƏSDİQLƏNDİ** | mfa/sso düzgün stub |
| 2 — Accounts (7) | ✅ TAMAMLANDI | 7/7 = 200 | **TƏSDİQLƏNDİ** | |
| 3 — Dashboard (4) | ✅ TAMAMLANDI | 3/4 (export 404) | **TƏSDİQLƏNMƏDİ** | /dashboard/export/ yoxdur |
| 4 — Evaluations (7) | ✅ TAMAMLANDI | 4/7 (forms/calibration/weights 404) | **TƏSDİQLƏNMƏDİ** | 3 səhifə yoxdur |
| 5 — Departments (3) | ✅ TAMAMLANDI | 3/3 = 200 | **TƏSDİQLƏNDİ** | |
| 6 — Reports (4) | ✅ TAMAMLANDI | 4/4 = 200 | **TƏSDİQLƏNDİ** | |
| 7 — Dev Plans (3) | ✅ TAMAMLANDI | 3/3 = 200 | **TƏSDİQLƏNDİ** | |
| 8 — Notifications (6) | ✅ TAMAMLANDI | 3/6 (templates 404) | **TƏSDİQLƏNMƏDİ** | email/sms/push-templates səhv yolda |
| 9 — Competencies (3) | ✅ TAMAMLANDI | 3/3 = 200 | **TƏSDİQLƏNDİ** | |
| 10 — Training (4) | ✅ TAMAMLANDI | 4/4 = 200 | **TƏSDİQLƏNDİ** | |
| 11 — Audit (6) | ✅ TAMAMLANDI | 6/6 = 200 | **TƏSDİQLƏNDİ** | |
| 12 — Workforce (2) | ✅ TAMAMLANDI | 2/2 = 200 | **TƏSDİQLƏNDİ** | |
| 13 — Feedback (3) | ✅ TAMAMLANDI | 3/3 = 200 | **TƏSDİQLƏNDİ** | |
| 14 — Workflow (6) | ✅ TAMAMLANDI | 0/6 planlaşdırılan yolda (404) | **TƏSDİQLƏNMƏDİ** | Səhv prefiks: /api/v1/workflow/ |
| 15 — Approval (5) | ✅ TAMAMLANDI | 0/5 planlaşdırılan yolda (404) | **TƏSDİQLƏNMƏDİ** | Səhv prefiks |
| 16 — Access Control (6) | ✅ TAMAMLANDI | 0/6 planlaşdırılan yolda (404) | **TƏSDİQLƏNMƏDİ** | Səhv prefiks + adlandırma + 🔴 qorunmasız |
| 17 — Policy Engine (5) | ✅ TAMAMLANDI | 0/5 planlaşdırılan yolda (404) | **TƏSDİQLƏNMƏDİ** | Səhv prefiks + 🔴 qorunmasız |
| 18 — Feature Flags (5) | ✅ TAMAMLANDI | 0/5 planlaşdırılan yolda (404) | **TƏSDİQLƏNMƏDİ** | Səhv prefiks |
| 19 — P-File (6) | ✅ TAMAMLANDI | 0/6 (hamısı 500) | **TƏSDİQLƏNMƏDİ** | NameError: '_' import edilməyib |
| 20 — Compensation (4) | ✅ TAMAMLANDI | 4/4 = 200 | **TƏSDİQLƏNDİ** | |
| 21 — Leave (5) | ✅ TAMAMLANDI | 5/5 = 200 | **TƏSDİQLƏNDİ** | |
| 22 — OKR (4) | ✅ TAMAMLANDI | 3/4 (check-ins 500) | **TƏSDİQLƏNMƏDİ** | FieldError select_related('user') |
| 23 — Recruitment (5) | ✅ TAMAMLANDI | 4/5 (referrals 500) | **TƏSDİQLƏNMƏDİ** | FieldError select_related('referred_by') |
| 24 — Sentiment (3) | ✅ TAMAMLANDI | 3/3 = 200 (stub) | **TƏSDİQLƏNDİ** | Prefiks /sentiment-analysis/ (plan /sentiment/) |
| 25 — Wellness (3) | ✅ TAMAMLANDI | 3/3 = 200 | **TƏSDİQLƏNDİ** | |
| 26 — Engagement (3) | ✅ TAMAMLANDI | 2/3 (anonymous-feedback 500) | **TƏSDİQLƏNMƏDİ** | FieldError 'created_at' |
| 27 — Support (6) | ✅ TAMAMLANDI | 5/6 (tickets/{id} 404 + detail 500) | **TƏSDİQLƏNMƏDİ** | Detail yolu yox + FieldError |
| 28 — Superuser (19) | ✅ TAMAMLANDI | 19/19 = 200 (stub) | **TƏSDİQLƏNDİ** | Hamısı stub; /admin→/admin-panel ad fərqi; qorunma düzgün ✅ |

**Yekun say:** 28 batch-dan **15 TƏSDİQLƏNDİ**, **13 TƏSDİQLƏNMƏDİ**.  
**URL yekunu:** 161-dən planlaşdırılan yolda **117 = 200**, **35 = 404**, **9 = 500**. (35 × 404-dən 26-sı `/api/v1/` altında faktiki mövcuddur, lakin planlaşdırılan/istifadəçi-üçün yolda deyil.)

---

# KÖK SƏBƏBLƏRİN XÜLASƏSİ

Fayllar mövcuddur, INSTALLED_APPS tam, migrasiyalar tətbiq olunub, konteyner sağlam, kod commit edilib. Buraxılmış addım **URL qeydiyyatı (routing) və view kodundakı 4 tip xəta**dır:

1. **Səhv URL prefiksi (28 URL — Batch 14-18):** engine app `urls.py`-ları `config/api_urls.py:366-370`-də `/api/v1/` altında include olunub, `config/urls.py:145-149`-də isə yalnız tək `dashboard/` səhifəsi olan `ui_urls.py`. Planlaşdırılan `/workflow/`, `/access-control/` və s. yollarda UI səhifələri yoxdur. + 🔴 təhlükəsizlik (yalnız `@login_required`).
2. **Import xətası (6 URL — Batch 19):** `apps/accounts/views_pfile.py`-də `gettext_lazy as _` import edilməyib → NameError → 500.
3. **ORM sahə xətaları (4 URL — Batch 22/23/26/27):** view-larda yanlış sahə adları (`select_related('user'/'referred_by')`, `filter(created_at)`) → FieldError → 500.
4. **Heç vaxt yaradılmamış səhifələr (7 URL — Batch 3/4/8):** `/dashboard/export/`, `/evaluations/forms/`, `/evaluations/weights/`, `/notifications/*-templates/` planlaşdırılan sadə formada mövcud deyil.

---

# DÜZƏLİŞ PLANI (yalnız təklif — bu tapşırıqda kod yazılmır)

1. **Batch 14–18 routing + təhlükəsizlik (ən yüksək prioritet):**
   - `config/urls.py`-də engine UI `urls.py`-larını düzgün prefiksdə include et (`path('workflow/', include('apps.workflow_engine.urls', ...))`), və ya UI səhifələrini `ui_urls.py`-a köçür.
   - `config/api_urls.py`-dan UI route-larını çıxar (API yalnız router-ləri saxlasın; UI ilə router-i qarışdırma).
   - 🔴 `apps/*/views_extras.py`-dakı `@login_required`-i superuser/permission decorator ilə əvəzlə (məs. `@user_passes_test(lambda u: u.is_superuser)`), Access Control/Policy Engine adi istifadəçiyə açıq qalmasın.
2. **Batch 19:** `apps/accounts/views_pfile.py` başına `from django.utils.translation import gettext_lazy as _` əlavə et.
3. **Batch 22/23/26/27:** sahə adlarını modelə uyğunlaşdır — OKR check-ins `'user'`→`'created_by'`, Recruitment referrals `'referred_by'`→`'referrer'`, Engagement anonymous-feedback `created_at`→`responded_at`, Support ticket detail `select_related('user')`→`'created_by'`.
4. **Batch 3/4/8:** Ya planlaşdırılan URL-ləri yarat, ya da naviqasiya/planı faktiki yollara (`/notifications/templates/emails/` və s.) uyğunlaşdır.
5. **STUB aydınlığı:** `designer/`, `simulator/`, `sentiment-analysis/history/` səhifələrinə görünən "Tezliklə" statusu əlavə et.
6. **Düzəlişdən sonra:** `verify_161.py`-i yenidən icra edib 161/161 = 200/302 və təhlükəsizlik testində 0×200 (adi istifadəçi) təsdiqlə.

---

## Metodologiya və məhdudiyyətlər
- Bütün statuslar Django test client (`force_login`) ilə konteyner daxilində alınıb, brauzerdə deyil.
- DEBUG=True olduğu üçün 500-lük xətalar test client-də exception kimi göründü (production-da HTTP 500).
- 2 müvəqqəti test istifadəçisi (`qa_tmp_regular_161`, `qa_tmp_regular_sec2`) yaradılıb test sonunda `delete()` ilə silindi; superuser `admin` mövcud idi (yaradılmadı). `git status` = yalnız bu hesabat faylı, kod dəyişikliyi yoxdur.
- Ekran görüntüsü əvəzinə render HTML mətn markeri yoxlanıldı (headless brauzer yoxdur). STUB HTML nüsxələri scratchpad-da saxlanılıb.
- İstifadə olunan skriptlər: `verify_161.py` (161 URL + təhlükəsizlik + STUB), `verify_alt.py` (404 alan yolların faktiki nüsxələri), `verify_sec_alt.py` (`/api/v1/` engine UI-lar üçün adi istifadəçi testi).
```
