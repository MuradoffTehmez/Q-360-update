# Q360 API Memarlığının Qurulması və Standartlaşdırılması

Hədəf: Q360 layihəsində olan bütün 22+1 (23) Django app-in API-lərinin tam şəkildə yazılması, vahid standarta salınması, `/api/v1/` versiyalaması ilə təmin edilməsi və `drf-spectacular` ilə sənədləşdirilməsi.

## User Review Required
> [!IMPORTANT]
> API versiyalaması olaraq `/api/v1/` prefiksi qəbul ediləcək. Geriyə uyğunluğu qorumaq üçün köhnə `/api/` path-ləri saxlanıla bilər və ya yeni sistemə miqrasiya tam şəkildə həyata keçiriləcək. Təsdiqinizdən sonra köhnə path-lərin alias olaraq saxlanması planlaşdırılır.

> [!WARNING]
> Hazırda bəzi modulların (məs: `onboarding`, `performance_reviews`, `reports`) API-ləri yazılıb amma router-ə qoşulmayıb. Onlar birbaşa yeni `/api/v1/` daxilinə qeydiyyatdan keçəcək.

## Proposed Changes

### HİSSƏ 1: API AUDİTİ VƏ İNVENTARİZASİYA
- [x] [API_INVENTORY.md](file:///C:/Users/Tahmaz%20Muradov/.gemini/antigravity-ide/brain/a2099113-ab61-436d-8c39-9a5f9caa7403/API_INVENTORY.md) yaradıldı və cari vəziyyət qeyd edildi.

### HİSSƏ 2: ÇATIŞMAYAN API-LƏRİN YARADILMASI
Siyahıdakı hər bir API-siz və ya natamam app üçün (xüsusən: `audit`, `dashboard`, `development_plans`, `notifications`, `search`, `security`, `sentiment_analysis`, `support`, `wellness`, `onboarding`, `performance_reviews`, `reports`):
- **Serializers**: Həssas məlumatları `SerializerMethodField` ilə filtrləyən serializer-lər yazılacaq.
- **ViewSets**: Standart `ModelViewSet` və uyğun permission (`IsAuthenticated`) sinifləri əlavə olunacaq.
- **Pagination & Filtering**: Standart `PageNumberPagination` və `django-filter` / DRF SearchFilter tətbiq olunacaq.
- **Router**: Hər modula `api_urls.py` (və ya `urls.py`) əlavə edilib əsas API routerinə qeyd ediləcək.

### HİSSƏ 3: API STANDARTLAŞDIRILMASI
- Xəta və uğur cavablarının eyni formata salınması üçün custom `Exception Handler` və `Renderers` və ya ViewSet bazası yazılacaq.
  - Success: `{"success": true, "data": {...}, "message": "..."}`
  - Error: `{"success": false, "error": "...", "code": "..."}`
- `/api/v1/` prefiksi `config/urls.py`-a əlavə ediləcək.
- `RateLimitMiddleware` yoxlanılacaq və endpointlər limitlərdən keçəcək.

### HİSSƏ 4: SWAGGER/REDOC SƏNƏDLƏŞDİRMƏSİ
- `drf-spectacular` quraşdırılması (əgər yoxdursa) və `SPECTACULAR_SETTINGS` konfiqurasiyası.
- Bütün əsas ViewSet-lərdə `@extend_schema` dekoratorları ilə məlumat əlavə olunacaq.
- `/api/schema/swagger-ui/` əlçatan ediləcək və JWT/Token Auth Swagger-ə əlavə ediləcək.

### HİSSƏ 5: ƏLAVƏ SƏNƏDLƏŞDİRMƏ
- `docs/API_GUIDE.md` yazılacaq (Auth, Endpointlər, Error Code-lar, Curl nümunələri).
- `README.md` yenilənəcək.
- `Q360_Full_API.postman_collection.json` yaradılacaq.

### HİSSƏ 6: TAM REGRESSİYA VƏ API TESTİ
- Yeni DRF testləri yazılacaq (APITestCase).
- `docker compose exec web python manage.py test -v 2` çalışdırılaraq nəticə təsdiqlənəcək.
- Newman istifadə edərək əlavə API testləri icra olunacaq.

## Verification Plan
1. Hər modul əlavə edildikdən sonra `curl` sorğuları ilə (200 OK və 401/403) test ediləcək.
2. Sonda Django unit testləri (APITestCase) icra edilərək 0 FAIL əldə olunacaq.
3. Postman kolleksiyası vasitəsilə `newman` CLI testi icra ediləcək.
