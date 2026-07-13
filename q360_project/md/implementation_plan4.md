# API Konsolidasiyası və AllowAny Probleminin Analizi

## 1. TƏKRARLANAN ENDPOINT-LƏRİN İNVENTARİZASİYASI
Təhlil nəticəsində məlum oldu ki, hər iki struktur (`/api/v1/<modul>/...` və `/<modul>/api/...`) **TAMAMİLƏ EYNİ** ViewSet-lərə və eyni koda istinad edir. Heç bir halda (evaluations, reports, onboarding, və s.) ayrıca təkrarlanan ViewSet və ya Serializer yazılmayıb. Sadəcə olaraq eyni ViewSet həm `config/api_urls.py` faylında qeydiyyatdan keçib, həm də app-səviyyəli (məsələn, `apps/evaluations/urls.py`) fayllarda yenidən DefaultRouter vasitəsilə `api/` path-inə qoşulub.
Buna görə də köhnə path-ləri silmək funksionallıq itkisi yaratmayacaq.

## 2. ALLOWANY PROBLEMİNİN KÖK SƏBƏBİ
- **Global permission:** `settings.py`-da `DEFAULT_PERMISSION_CLASSES` olaraq `rest_framework.permissions.IsAuthenticated` təyin edilib.
- **Kök səbəb:** Problem DRF-in `@permission_classes([AllowAny])` dekoratorunun işləməməsində deyil. Kök səbəb layihədəki **Daphne (ASGI) serverinin** avtomatik *reload* xüsusiyyətinin olmamasıdır (`runserver` kimi deyil). Mən ilk dəfə `api_root` funksiyasını yazanda dekoratorsuz yazmışdım və qlobal `IsAuthenticated` işə düşmüşdü. Daha sonra `@permission_classes([AllowAny])` əlavə etsəm də, konteyner restart edilmədiyi üçün yaddaşda (memory) hələ də köhnə kod icra olunurdu. Buna görə də `curl` sorğuları həmişə DRF tərəfindən 401 ilə bloklanırdı.
- **Düzgün Həll:** DRF-dən imtina edib `JsonResponse` yazmaq əvəzinə, orijinal DRF `@api_view` həllini geri qaytarıb və konteyneri restart edərək, standart bir public API endpoint formatını qoruyacağam.

## 3. KONSOLİDASİYA PLAN (İcra Ediləcək Dəyişikliklər)

Aşağıdakı modulların app-level `urls.py` fayllarından `path('api/', include(router.urls))` sətirləri TAMAMİLƏ silinəcək:
- `apps/evaluations/urls.py`
- `apps/reports/urls.py`
- `apps/onboarding/urls.py`
- `apps/performance_reviews/urls.py`
- `apps/workforce_planning/urls.py`
- `apps/continuous_feedback/urls.py`
- `apps/dashboard/urls.py`

**Frontend Dəyişiklikləri (Template-lər və JS fayllar):**
Mövcud frontend axtarışımın nəticəsinə əsasən köhnə API yollarına müraciət edən aşağıdakı frontend sorğuları yenilənəcək:
- `templates/onboarding/template_library.html` -> `/api/v1/onboarding/templates/`
- `templates/reports/schedule_center.html` -> `/api/v1/reports/schedules/`
- `templates/reports/team_reports.html` -> `/api/v1/evaluations/campaigns/`
- `static/js/dashboard.js` -> `/api/v1/dashboard/...`
- Və grep ilə tapılmış digər hər hansı `/<modul>/api/...` müraciətləri.

## 4. VERİFİKASİYA VƏ REGRESSİYA PLANI
- `api_root` yenidən DRF formatına keçiriləcək, konteyner restart ediləcək və işlədiyi `curl` sübutu ilə göstəriləcək.
- Silinən köhnə URL-lər üçün 404 xətası verildiyi yoxlanılacaq.
- Yenilənmiş `/api/v1/` URL-lərin isə 200 OK qaytardığı sübut ediləcək.
- `docker compose exec web python manage.py test -v 2` işə salınaraq testlərin 100% keçdiyi göstəriləcək. Əgər test fayllarında köhnə path-lərə istinad varsa, onlar da yenilənəcək.
