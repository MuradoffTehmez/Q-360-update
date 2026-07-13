# Q360 Layihəsi: Bugların Həlli və Arxitektura Təkmilləşdirmə Planı (Tam)

Bu plan istifadəçi tərəfindən aşkar edilmiş bütün 20 bug (Blok A-dan E-yə qədər) və memarlıq problemlərinin həlli üçün atılacaq konkret addımları əhatə edir.

## User Review Required
> [!IMPORTANT]
> Aşağıdakı plan bütün boşluqları və əvvəllər təyin edilmiş bug-ların kök səbəblərini əhatə edir. Kodlaşdırma mərhələsinə keçmək üçün bu planı təsdiqləməyiniz xahiş olunur (məsələn, "Təsdiqləyirəm, kodu yazmağa başla").

---

## 1. BLOK A: Kritik Funksionallıq və DB Xətaları

### 1.1 `/reports/catalog/` (NoReverseMatch)
- **Kök səbəb:** `template_views.py`-da `detailed-report` URL-i üçün `<int:result_pk>` tələb olunur, lakin template-də sadəcə ID ötürülür və ya ID mövcud deyil.
- **Həll:** `catalog.html`-də `href="{% url 'reports:detailed-report' result_pk=report.id %}"` formasında düzəliş etmək (Artıq qismən düzəldilib).

### 1.2 `/audit/logs/` (NoReverseMatch)
- **Kök səbəb:** `log_search.html` template-də form action boşdur və ya URL name-də xəta var (`{% url 'audit:log-search' %}` ola bilsin düzgün deyil).
- **Həll:** `apps/audit/urls.py` və `log_search.html` fayllarında namespace və URL adlarının tam uyğunluğunu yoxlayıb uyğunlaşdırmaq.

### 1.3 `LeaveRequest` (Tarix formatı xətası)
- **Kök səbəb:** Model/Serializer səviyyəsində `YYYY-MM-DD` əvəzinə `MM/DD/YYYY` formatında data gəlir və ya form validation xətası verir.
- **Həll:** `apiSubmit` istifadə edildiyi üçün, frontend-də JS vasitəsilə tarixi standart ISO formatına salıb göndərmək.

### 1.4 `Report` və `FeedbackBank` Modeli (generated_by validation)
- **Kök səbəb:** `generated_by` sahəsi daxili məntiqdə doldurulur, lakin form/serializer səviyyəsində `required=True` olduğu üçün DB-yə çatmadan validation fail olur.
- **Həll:** `models.py`-da `blank=True, null=True` edilmişdir, serializer səviyyəsində də `read_only=True` təyin etmək.

---

## 2. BLOK B: Qalan CRUD Əməliyyatlarının Tamamlanması

Aşağıdakı bölmələrdə natamam qalan (və ya ümumiyyətlə olmayan) CRUD prosesləri tamamlanacaq:

### 2.1 `/training/my-trainings/` və `/competencies/my-skills/`
- **Kök səbəb:** Mövcud siyahı (List) görünüşü var, lakin yeni təlim/bacarıq əlavə etmək üçün View, Form və ya endpoint təyin edilməyib, həmçinin template-də "Create" düyməsinə kliklədikdə heç nə baş vermir.
- **Həll Planı:**
  - `template_views.py`-da `training_create`, `skill_create`, `skill_edit` metodları yaradılacaq.
  - Müvafiq modal pəncərələr `my_trainings.html` və `my_skills.html` template-lərinə əlavə ediləcək.
  - Hər biri üçün `apiSubmit` vasitəsilə AJAX sorğuları bağlanacaq və nəticə olaraq cədvəl dinamik yenilənəcək.

### 2.2 `/feedback/360-feedback-request/`
- **Kök səbəb:** Rəy istəmə forması göndərildikdə, backend-də rəy sorğusunu (Feedback Request) yadda saxlayacaq serializer/view uyğunlaşdırılmayıb və ya 404/405 status verir.
- **Həll Planı:** `feedback_request_create` üçün POST endpoint yazılacaq, frontend-də Alpine.js/Vanilla JS form submit intercept edilib JSON olaraq göndəriləcək.

### 2.3 `/evaluations/my-assignments/` (Boş Cədvəl Problemi)
- **Kök səbəb:** Səhifə yüklənir, lakin istifadəçiyə aid heç bir `EvaluationAssignment` görünmür. Çünki `EvaluationAssignment` modeli yaradılarkən istifadəçilərə (evaluatee/evaluator) assignment-lər avtomatik təyin olunmayıb və ya filter statusa görə səhvdir.
- **Həll Planı:** Cədvəlin filter məntiqini (status='pending' vs 'all') nəzərdən keçirmək. Zərurət olarsa, dashboard yüklənəndə nümunəvi təyinatlar (seed) yaradan düymə əlavə etmək və ya admin paneldən daxil edilən təyinatların view-da düzgün `request.user`-ə uyğun filterləndiyinə əmin olmaq (`evaluator=request.user` vs `evaluatee=request.user`).

### 2.4 `/reports/schedules/` və `/reports/blueprints/.../`
- **Kök səbəb:** Blueprint daxilində qrafiklər və report planlaması üçün frontend UI (düymələr, cədvəl) var, lakin backend CRUD tam yazılmayıb (məs. `/blueprints/<slug>/visualizations/add/` yalnız GET üçün işləyir və ya save etmir).
- **Həll Planı:**
  - `schedule_create` endpointi backend-də yaradılacaq və `Celery` tapşırığı kimi planlanacaq.
  - `blueprint_visualization_add` və `_delete` üçün AJAX ilə idarə olunan formalar yazılacaq.

### 2.5 `/onboarding/templates/`
- **Kök səbəb:** Bu səhifə template olaraq tamamilə yoxdur və ya 404 qaytarır.
- **Həll Planı:** `onboarding/templates.html` səhifəsi sıfırdan Bootstrap UI ilə hazırlanacaq, list və create view-ları əlavə ediləcək.

---

## 3. BLOK C: Data Sinxronizasiyası və Real-Time Xətaları

### 3.1 `/leave/attendance/?month=`
- **Kök səbəb:** URL parametrindəki `month` dəyəri view tərəfindən qəbul edilib `datetime` filterinə düzgün ötürülmür (string kimi qalır və format exception verir).
- **Həll Planı:** `template_views.py`-da `month` parametrini try-except bloku ilə `int`-ə çevirmək və QuerySet filterində `__month` və `__year` olaraq ayırmaq.

### 3.2 `/accounts/profile/edit/` (Multipart form)
- **Kök səbəb:** Profil şəklini yeniləmək üçün formda `enctype="multipart/form-data"` eksikdir, ya da `apiSubmit` fayl upload-ı JSON kimi göndərməyə çalışır.
- **Həll Planı:** Forma `enctype` əlavə ediləcək, `apiSubmit` JS funksiyası fayl göndərilirsə avtomatik olaraq `FormData` obyektinə keçib `Content-Type`-ı brauzerə buraxacak şəkildə modifikasiya ediləcək.

### 3.3 `/accounts/profile/` (Stale Data)
- **Kök səbəb:** Məlumat yeniləndikdən sonra page refresh olmadan köhnə məlumatlar UI-da qalır və ya backend keşdə saxlayır.
- **Həll Planı:** `ProfileUpdateView` POST ugurlu olduqda yeni profil detallarını JSON olaraq qaytaracaq, frontend DOM-da dərhal yeniləyəcək.

### 3.4 `/notifications/settings/`
- **Kök səbəb:** Checkbox-lar (email/push/sms) state dəyişəndə backend-ə sorğu getmir.
- **Həll Planı:** `change` event listener əlavə edilib `apiSubmit` vasitəsilə PATCH sorğusu ilə istifadəçi parametrlərini avtomatik yadda saxlamaq.

### 3.5 `/notifications/inbox/` (WebSocket Problemi)
- **Kök səbəb:** `notifications.js` faylı `document.querySelector('[data-user-id]') !== null` şərtini yoxlayaraq WebSocket bağlantısını qurur. Lakin heç bir HTML template-də (o cümlədən `base.html`-də) `data-user-id` elementi yoxdur. Nəticədə `connectWebSocket()` funksiyası HƏÇ VAXT işə düşmür, server isə notification göndərməyə çalışdıqda client bağlantısı olmur.
- **Həll Planı:** `base.html`-də `<body>` tag-inə və ya uyğun meta tag-ə `<body data-user-id="{{ request.user.id }}">` əlavə ediləcək.

---

## 4. BLOK D: UI/UX Dizayn və Template Render Xətaları

### 4.1 `/accounts/security/` (Şifrə dəyişmə və CSS/JS konflikti)
- **Kök səbəb (Konflikt):** Şifrə göstər/gizlət Javascript kodu (`toggle-password`) birbaşa `.previousElementSibling` axtarır. Şifrə dəyişmə uğursuz olduqda Django inputun ətrafına `<ul class="errorlist">` əlavə edir, bu zaman DOM strukturu pozulur və JS xəta verir.
- **Kök səbəb (Submit problemi):** Formun action-u `{% url 'accounts:change-password' %}` endpointinə baxır, lakin bu view `security_settings` view-u ilə eynidir. Validation error olduqda view yenidən `accounts/security.html` render edir və brauzerdəki URL dəyişir, bu isə sonrakı əməliyyatların (MFA setup və s.) eyni ünvana səhv POST edilməsinə səbəb olur.
- **Həll Planı:** Şifrə dəyişmə əməliyyatını xüsusi bir API endpointinə (`/accounts/api/change-password/`) yönləndirib, `apiSubmit` vasitəsilə AJAX ilə emal etmək və CSS DOM strukturunu sabit saxlamaq.

### 4.2 `/audit/security-dashboard/` (Timestamp render problemi və CRUD)
- **Kök səbəb:** View-da backend-dən qaytarılan tarix `recent_failures_data` içində `f.created_at.isoformat()` vasitəsilə string olaraq qaytarılır. Template-də isə string üzərində Django-nun `|date:"d M Y H:i"` filteri tətbiq edilir. Bu filter yalnız `datetime` obyektlərində işlədiyinə görə, string-lə qarşılaşanda səssizcə fail olur və heç nə render etmir (boş çıxır).
- **Həll Planı:** View-da obyekti ISO formatına yox, birbaşa `.strftime()` vasitəsilə düzgün string-ə çevirib template-ə ötürmək, yaxud template-də filteri ləğv etmək. Əlavə olaraq IP Block/Unblock düymələri üçün AJAX CRUD qarmaqları artırılacaq.

### 4.3 `/reports/custom-builder/` (Chart Yenilənməsi və Drag & Drop UX)
- **Kök səbəb (Chart.js vs Plotly):** Hazırda `custom_report_view.html` Plotly istifadə edərək qrafik render edir, lakin istifadəçi report qurduqda form məlumatı ilə POST etmədikcə vizual preview görə bilmir. JS-də chart library-i üçün heç bir real-time `onChange` update funksiyası mövcud deyil.
- **Kök səbəb (Drag & Drop UX):** `custom_report_builder.html`-də Drag & Drop sadə Vanilla JS (`event.dataTransfer`) ilə qurulub, vizual feedback zəifdir.
- **Həll Planı:**
  - Builder səhifəsində seçilmiş chart tipinə əsasən kiçik canlı (live) qrafik nümunəsi (Plotly `react`) göstərən JS listener əlavə etmək.
  - Sütunların Drag & Drop UX-ni inkişaf etdirmək üçün HTML5 daxili eventləri əvəzinə hamar hərəkət üçün CSS transition-lar və ya lazımdırsa kiçik `SortableJS` tərzində məntiq (əgər Alpine.js imkan verirsə) istifadə etmək.

---

## 5. BLOK E: Arxitektura / CSRF
- **Cari Status:** JS tərəfində qlobal `apiSubmit` və `getCookie` yazılıb, `X-CSRFToken` header-i avtomatlaşdırılıb. (Faza 2-də artıq qismən implementasiya edilib).
- **Həll Planı:** Bu qlobal struktur yeni yazılacaq bütün formlarda (Blok B və C) istifadə edilərək təkrar kodun qarşısı alınacaq. Hər bir AJAX çağırışı eyni CSRF error-handler-dən keçəcək.

## 6. Verification Plan
*   **Automated Tests:** `test_part2_celery.py` və oxşar testləri çalışdırıb xətaların azaldığını görmək.
*   **Manual Verification:**
    *   Sistemə daxil olub `<body data-user-id="...">` elementinin varlığını və WebSocket bağlantısının console-da `Connected` olmasını yoxlamaq.
    *   `/accounts/security/` səhifəsində yanlış şifrə yazıb AJAX xətasının qırmızı border/mətn kimi gəldiyini, lakin DOM-u pozmadığını təsdiqləmək.
    *   `/audit/security-dashboard/` səhifəsində tarixlərin düzgün yazıldığını gözlə görmək.
    *   Bütün yeni CRUD səhifələrində "Save" klikləyib `apiSubmit` vasitəsilə reload olmadan listin yeniləndiyini Docker terminalında HTTP 200 logu ilə sübut etmək.
