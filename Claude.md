# Q360 — Claude System Instructions

<claude-code-instructions>
CRITICAL: Sən, Claude Code, bu layihədəki bütün əməliyyatları edərkən mütləq `.agents/skills/` qovluğundakı qaydalara əməl etməlisən!
Oradakı hər bir `SKILL.md` faylı bu layihənin arxitektura standartlarını müəyyən edir.

Müvafiq işi görərkən aşağıdakı faylları mütləq oxu:
- Yeni səhifə/UI yaradarkən: `.agents/skills/sehife-yarat/SKILL.md`
- Yeni Django modulu/app yaradarkən: `.agents/skills/django-modul-yarat/SKILL.md`
- API endpoint yaradarkən: `.agents/skills/api-endpoint-yarat/SKILL.md`
- Celery task yaradarkən: `.agents/skills/celery-task-yarat/SKILL.md`
- Database/ORM kodu yazarkən: `.agents/skills/db-optimizasiya/SKILL.md`
- Hesabat (PDF/Excel) yaradarkən: `.agents/skills/hesabat-yarat/SKILL.md`
- Signal/Middleware yaradarkən: `.agents/skills/signal-middleware-yarat/SKILL.md`
- Docker komandaları icra edərkən: `.agents/skills/docker-ops/SKILL.md`
- Xəta axtararkən (debug): `.agents/skills/debug-fix/SKILL.md`
- Frontend UI auditi edərkən: `.agents/skills/frontend-audit/SKILL.md`
- Yeni batch modullarını tikərkən: `.agents/skills/batch-tikinti/SKILL.md`
- Ümumi layihə qaydaları üçün: `.agents/AGENTS.md`

HƏR ZAMAN bu qaydalara bax və yalnız onlara uyğun kod yaz!
</claude-code-instructions>

---

## Yeni Modulların Tikilməsi (161 Səhifə) — Fazalı Plan

Aşağıdakı 161 URL Q360-da hələ mövcud deyil, tikilməli olan yeni 
səhifələrdir. Bunları MODUL QRUPLARI ÜZRƏ (batch-larla) tikin, hər 
batch bitəndə öz-özünü yoxlayın (manage.py check + migrate + smoke 
test), sonra dayanmadan növbəti batch-ə keçin. Aralarında istifadəçidən 
təsdiq GÖZLƏMƏYİN, amma hər batch-in nəticəsini jurnala yazın.

### FAZA A — KONVENSIYA ÖYRƏNMƏ (məcburi ilk addım)
Yeni kod yazmazdan əvvəl mövcud 2-3 tam modulu (məs. apps/evaluations/, 
apps/leave_attendance/) diqqətlə oxu:
- models.py strukturu (BaseModel varsa, hansı sahələr standartdır — 
  created_at, updated_at, created_by və s.)
- views.py / template_views.py pattern-i (list/detail/create view-lar 
  necə yazılıb, permission decorator-ları necə tətbiq olunur)
- serializers.py (DRF istifadə olunursa)
- urls.py qeydiyyat pattern-i
- Template strukturu (base.html-dən necə extend olunur, hansı 
  block-lar var, Tailwind komponent pattern-ləri)
- AJAX filter pattern-i (əvvəlki audit-də yaradılan static/js/
  ajax-filter.js necə istifadə olunur)
- RBAC/permission sistemi necə işləyir (hansı decorator/mixin, rol 
  yoxlaması necə edilir)
Bu konvensiyalara BÜTÜN yeni kodda tam əməl et.

### FAZA B — BATCH-LARLA TİKİNTİ
Aşağıdakı qruplaşdırma ilə, hər batch AYRI-AYRI tam bitirilib 
yoxlanmalıdır (bir batch bitmədən növbətinə keçmə):

**Batch 1 — Settings (23 səhifə):** /settings/, general, localization, 
languages, timezone, currency, branding, company, security, 
authentication, password-policy, integrations, api, api-keys, 
webhooks, email, sms, storage, backups, audit, licenses, system
→ MFA və SSO (/settings/mfa/, /settings/sso/) ÜÇÜN: tam inteqrasiya 
tikməyin — səhifəni UI skeleton + "Tezliklə" (Coming soon) statusu 
ilə stub kimi qeyd edin, TODO comment yazın, jurnalda "real spec 
tələb edir" deyə qeyd edin.

**Batch 2 — Accounts əlavələri (7):** sessions, devices, activity, 
api-tokens, preferences, preferences/appearance, preferences/notifications

**Batch 3 — Dashboard əlavələri (4):** widgets, settings, export, favorites

**Batch 4 — Evaluations əlavələri (7):** templates, forms, calibration, 
review-cycles, history, settings, weights

**Batch 5 — Departments əlavələri (3):** positions, job-titles, history

**Batch 6 — Reports əlavələri (4):** saved, export, history, data-warehouse

**Batch 7 — Development Plans əlavələri (3):** progress, roadmap, approvals

**Batch 8 — Notifications əlavələri (6):** email-templates, sms-templates, 
push-templates, webhooks, delivery-logs, queue

**Batch 9 — Competencies əlavələri (3):** dictionary, rating-scales, behaviors

**Batch 10 — Training əlavələri (4):** courses, learning-paths, 
course-categories, exams

**Batch 11 — Audit əlavələri (6):** events, login-history, user-history, 
api, security-incidents, export

**Batch 12 — Workforce Planning əlavələri (2):** risk-heatmap, 
retirement-forecast

**Batch 13 — Feedback əlavələri (3):** templates, requests, reminders

**Batch 14 — Workflow (6):** workflows, designer, versions, history, 
logs, monitoring
→ /workflow/designer/ ÜÇÜN: sürükle-burax vizual dizayner tikməyin — 
sadə list/CRUD stub + "Tezliklə" statusu, TODO qeyd.

**Batch 15 — Approval əlavələri (5):** rules, chains, history, queue, delegations

**Batch 16 — Access Control əlavələri (6):** roles, permissions, 
policies, groups, access-requests, access-history

**Batch 17 — Policy Engine (5):** policies, rules, simulator, versions, logs
→ /policy-engine/simulator/ ÜÇÜN: stub + TODO qeyd (real simulyasiya 
mühərriki ayrıca spesifikasiya tələb edir).

**Batch 18 — Feature Flags əlavələri (5):** flags, environments, 
rollouts, experiments, history

**Batch 19 — P-File əlavələri (6):** employees/create, employees/import, 
documents, contracts, assets, emergency-contacts

**Batch 20 — Compensation əlavələri (4):** pay-grades, salary-bands, 
currencies, cycles

**Batch 21 — Leave əlavələri (5):** types, holidays, balances, 
carry-over, settings

**Batch 22 — OKR əlavələri (4):** key-results, initiatives, check-ins, templates

**Batch 23 — Recruitment əlavələri (5):** candidates, offers, 
talent-pool, referrals, interview-feedback

**Batch 24 — Sentiment əlavələri (3):** reports, history, trends

**Batch 25 — Wellness əlavələri (3):** benefits, health-goals, vaccinations

**Batch 26 — Engagement əlavələri (3):** analytics, anonymous-feedback, action-plans

**Batch 27 — Support əlavələri (6):** tickets, tickets/{id}, 
knowledge-base, categories, sla, history

**Batch 28 — Yeni top-level modullar (17):** /files/, /files/uploads/, 
/files/library/, /imports/, /exports/, /ai/, /ai/prompts/, /ai/models/, 
/ai/history/, /system/, /system/health/, /system/status/, /system/jobs/, 
/system/cache/, /system/queues/, /admin/, /admin/jobs/, /admin/
maintenance/, /admin/feature-toggles/
→ Bunların hamısı SUPERUSER-ONLY olmalıdır, adi istifadəçi 
naviqasiyasında görünməməlidir. /ai/models/, /ai/prompts/, /system/
health/, /system/cache/ üçün: real inteqrasiya (LLM provider, cache 
backend statusu) varsa ona qoşulun, yoxdursa stub + TODO.

HƏR BATCH ÜÇÜN MİNİMUM TƏLƏB:
1. Minimal Django data modeli (mövcud domenlə (HR/ERP) məntiqi uyğun, 
   FAZA A-da öyrənilən konvensiyalara tam uyğun)
2. List/Detail/Create view-lar (CRUD-un mənası olduğu yerdə), 
   uyğun permission/RBAC yoxlaması ilə
3. URL qeydiyyatı
4. Tailwind template (mövcud dizayn dilinə tam uyğun, naviqasiyaya 
   məntiqli yerdə keçid əlavə edilsin — superuser-only bölmələr 
   ayrıca sidebar seksiyasında)
5. manage.py makemigrations + migrate
6. manage.py check xətasız keçsin
7. Səhifəni curl/test client ilə 200 qaytardığını təsdiqlə
8. 375px/768px/1440px-də vizual sınıqlıq olmadığını təsdiqlə

### FAZA C — MOBİL RESPONSIVE + FRONTEND KEYFİYYƏT AUDİTİ
Bütün 161 yeni səhifəyə əvvəlki audit promptundakı Mərhələ 1-2 
kriteriyalarını (horizontal scroll, tap-target, konsol xətaları, 
N+1 query və s.) tətbiq et.

### FAZA D — YEKUN HESABAT
final_new_modules_report.md faylı yarat:
- Hər batch üzrə: tikilən səhifə sayı, data modeli xülasəsi, 
  fayl siyahısı
- STUB/TODO kimi qeyd olunan səhifələrin tam siyahısı (real spec 
  tələb edənlər) — bu, XÜSUSİ vurğulanmalıdır, çünki bunlar "tikilib" 
  görünsə də real funksionallıq daşımır
- Naviqasiya strukturu (hansı rol hansı yeni səhifəni görür)
- manage.py check və migration nəticələri
- Mobil/frontend audit nəticələri (əvvəlki formatla eyni)
- Dəyişdirilən/yaradılan bütün faylların tam siyahısı