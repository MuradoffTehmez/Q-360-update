# Q360 REST API Təlimatı

Bu sənəd Q360 layihəsində istifadə edilən REST API xidmətləri, onların inteqrasiyası, identifikasiyası və limitləri haqqında tam məlumat verir.

## 1. Əsas Məlumatlar

- **Base URL:** `http://<your-domain>/api/v1/`
- **Format:** Bütün request və response-lar yalnız `application/json` formatındadır.
- **Sənədləşdirmə:**
  - Swagger UI: `http://<your-domain>/api/schema/swagger-ui/`
  - Redoc UI: `http://<your-domain>/api/schema/redoc/`
  - OpenAPI YML: `http://<your-domain>/api/schema/`

## 2. Autentifikasiya (Authentication)

Sistem eyni vaxtda **iki fərqli autentifikasiya** sxemini dəstəkləyir (`SessionAuthentication` və `JWTAuthentication`). Bütün endpoints üçün uyğun başlıq və ya cookie tələb olunur.

### 1. Session Autentifikasiyası (Brauzer / Veb İnterfeys üçün)
Django-nun standart daxili interfeysi, Admin panel və eyni domendə işləyən daxili JavaScript/HTML UI üçün istifadə olunur.
- Sistemin veb səhifəsindən (məs: `/accounts/login/` üzərindən) daxil olduqda işə düşür.
- Əlavə API başlıqlarına (headers) ehtiyac yoxdur, brauzer sessiya məlumatlarını cookie vasitəsilə (`sessionid` və `csrftoken`) avtomatik göndərir.
- Təhlükəsizlik üçün POST/PUT/DELETE/PATCH sorğularında `X-CSRFToken` başlığı tələb edilə bilər.

### 2. JWT Autentifikasiyası (Mobil Tətbiq və Xarici Client-lər üçün)
Kənar tətbiqlər, mobil proqramlar və Postman kimi test alətləri üçün istifadə olunur. API-yə qoşulmaq üçün sorğu başlığına Token əlavə edilməlidir:

```http
Authorization: Bearer <access_token>
```

#### Token Alınması (JWT üçün)
POST `/api/auth/token/`
- Payload: `{"username": "your_username", "password": "your_password"}`
- Qayıdır: `access` və `refresh` tokenləri.

### Token Yenilənməsi
POST `/api/auth/token/refresh/`
- Payload: `{"refresh": "your_refresh_token"}`

## 3. Limitlər (Rate Limiting)

DDoS və brute-force hücumlarının qarşısını almaq üçün sistemdə API limitləri tətbiq edilmişdir:

- **Login / Token Endpointləri:**
  - `LoginThrottle`: Dəqiqədə maksimum 5 cəhd (`5/min`).
- **Ümumi API Zəngləri:**
  - Anonim istifadəçilər: Günlük limit və ya IP limit (`AnonRateThrottle`).
  - Qeydiyyatlı istifadəçilər: Standart istifadəçilər üçün dəqiqə və günlük limitlər.
  Limit aşılarsa API `429 Too Many Requests` xətası qaytaracaq.

## 4. Response Formatları və Xətalar

Standart müvəffəqiyyət (`200 OK`, `201 Created`):
Payload birbaşa və ya pagination əlavə edilərək qaytarılır.

Standart Xətalar:
- `400 Bad Request`: Yanlış məlumat.
- `401 Unauthorized`: Token yoxdur və ya vaxtı keçib.
- `403 Forbidden`: Bu əməliyyat üçün hüququnuz (rolunuz) çatmır (məsələn, admin deyil).
- `404 Not Found`: Resurs tapılmadı.
- `429 Too Many Requests`: Limit aşıldı.
- `500 Internal Server Error`: Server daxili xəta.

## 5. Pagination & Filtrləmə

- **Pagination:**
  Varsayılan olaraq bütün list endpointləri `PageNumberPagination` (və ya layihədə seçilmiş standart) istifadə edir.
  `?page=1&page_size=10`
- **Filtrləmə:**
  URL üzərindən filtrləmə dəstəklənir (məs: `?status=active`, `?department=IT`).
- **Axtarış (Search):**
  `?search=keyword` vasitəsilə təyin edilmiş sahələrdə axtarış aparıla bilər.
- **Sıralama (Ordering):**
  `?ordering=-created_at` vasitəsilə spesifik sahələrə görə çeşidləmə mümkündür.

## 6. Endpoints İcmalı

Sistemdəki əsas modullar və API seqmentləri:

- **/api/v1/accounts/** - İstifadəçi idarəetməsi, rollar və PFile.
- **/api/v1/departments/** - Təşkilati struktur, şöbələr, regionlar.
- **/api/v1/evaluations/** - Qiymətləndirmələr, suallar, kampaniyalar.
- **/api/v1/recruitment/** - Vakansiyalar, müraciətlər, müsahibələr.
- **/api/v1/leave/** - Məzuniyyət sorğuları, balans və iştirak uçotu.
- **/api/v1/training/** - Təlim resursları və istifadəçi təlimləri.
- **/api/v1/performance-reviews/** - 1x1 iclaslar, tapşırıqlar və rəylər.
- **/api/v1/compensation/** - Əməkhaqqı paketləri, bonuslar, tarixçə (şifrələnmiş).

Tam interaktiv sənədləşdirmə və endpointlərin dəqiq cədvəli üçün Swagger UI panelini ziyarət edin.
