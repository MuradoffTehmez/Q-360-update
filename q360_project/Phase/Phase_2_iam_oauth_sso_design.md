# Phase 2 - Identity & Access Management (OAuth2, SSO, API Keys)

## 1. Məqsəd
Sistemə təhlükəsiz və standartlaşdırılmış giriş yollarını təmin etmək. Q360-ı fərqli korporativ platformalarla (Məs: Microsoft Active Directory, Google Workspace) inteqrasiya edərək tək hesab (Single Sign-On - SSO) ilə girişi təmin etmək. Üçüncü tərəf sistemlər (Server-to-Server) üçün təhlükəsiz API Key və ya OAuth2 infrastrukturunu qurmaq.

## 2. Biznes məqsədi
İstifadəçilərin hər proqram üçün fərqli parol yadda saxlamaq məcburiyyətini aradan qaldırmaq, şirkətin mərkəzi parollar siyasətinə (məs: hər 3 aydan bir dəyişməli) avtomatik uyğunlaşmaq. Digər tətbiqlərin Q360 API-lərinə təhlükəsiz və qeydiyyatlı şəkildə inteqrasiya etməsinə icazə vermək (B2B).

## 3. Arxitektura
- **OAuth2 Provider:** Django daxilində Q360-ı həm Identity Provider (IdP) həm də Service Provider (SP) kimi istifadə edə bilmək üçün `django-oauth-toolkit` inteqrasiyası.
- **SSO (OIDC / SAML):** Təşkilatın daxili Active Directory-si (və ya Azure AD, Okta, Google) ilə əlaqə.
- **API Key Management:** Xidmət hesabları (Service Accounts) üçün son istifadə müddəti olan və idarə edilə bilən API tokenlər.

## 4. Modul strukturu
```text
q360_project/apps/identity_management/
├── models/
├── services/
├── api/
│   ├── serializers/
│   └── views/
├── auth_backends/ (SSO və API Key üçün custom backendlər)
└── tests/
```

## 5. Database dəyişiklikləri
### Yeni cədvəllər
- OAuth2 toolkitin öz cədvəlləri (`oauth2_provider_application`, `oauth2_provider_accesstoken`, s.)
- `api_key` (Server-to-server inteqrasiyalar üçün ad, prefix, hashed key, expiry date)
- `sso_provider` (Dinamik SSO konfiqurasiyaları: Client ID, Secret, Discovery URL)
- `user_sso_identity` (Q360 istifadəçisi ilə xarici IdP istifadəçisi arasındakı əlaqə/mapping)

### Əlaqələr və Constraints
- API Keylər `User` modelinə yox, xüsusi yaradılmış "Service Account" (Robot istifadəçi) modelinə bağlanmalıdır.

## 6. API dəyişiklikləri
- **Yeni endpointlər:**
  - `POST /api/v1/auth/token/` (OAuth2 token endpointi)
  - `GET /api/v1/auth/sso/login/{provider_id}/` (İstifadəçini Microsoft/Google səhifəsinə yönləndirmək üçün)
  - `GET /api/v1/auth/sso/callback/` (OIDC cavabını qəbul edən endpoint)
  - `POST /api/v1/apikeys/` (Developerlərin özlərinə API Key yaratması)

## 7. Servislər (Service Layer)
- `SsoIntegrationService`: OIDC qeydiyyatlarını yoxlayan və əgər istifadəçi bazada yoxdursa avtomatik yaradan (Just-In-Time Provisioning) servis.
- `ApiKeyService`: API key-in generasiyası (sadəcə yaradıldıqda 1 dəfə açıq görünür, sonra isə ancaq bcrypt/argon2 ilə hash-i saxlanılır).

## 8. Permission modeli
- Xarici tətbiqlər (OAuth2 Client) yalnız istifadəçinin onlara verdiyi icazələr çərçivəsində (Scope - məs. `read:user_profile`, `write:leave_request`) əməliyyat edə bilər.

## 9. Workflow
SSO ilə giriş: İstifadəçi "Login with Microsoft" düyməsini sıxır -> Azure AD-yə yönlənir -> Təsdiqdən sonra Callback URL-ə qayıdır -> `SsoIntegrationService` tokeni yoxlayır və istifadəçini Q360-da daxil olmuş kimi qeyd edərək JWT tokeni Front-End-ə verir.

## 10. Event-lər
- `UserSSOLoggedIn`
- `ApiKeyCreated`
- `ApiKeyRevoked`

## 11. Security
- API Keylər heç vaxt bazada açıq mətn (plain text) formatında saxlanılmayacaq, eynilə parollar kimi hash ediləcək. Token oxumaq üçün prefix axtarılacaq.
- Scope validation: OAuth2 tokenləri yalnız icazə verilən əhatə dairəsində (Scope) API-lərə çata biləcək.

## 12. Logging
- Bütün uğursuz login və SSO inteqrasiya xətaları detallı şəkildə (Error traceback olmadan, sadəcə biznes məntiqi ilə) loglanacaq.

## 13. Audit
- API Key-in kim tərəfindən nə vaxt ləğv edildiyi mütləq loqlanacaq.

## 14. Performance
- Authentication middleware-də hər API müraciətində bazadan API key yoxlamaq ağır əməliyyatdır. Aktiv API Key hash-ləri Redis-də cache-də saxlanılmalıdır.

## 15. Background process
- Vaxtı bitmiş API Keylərin avtomatik silinməsi və ya passiv edilməsi (Celery Beat).

## 16. UI dəyişiklikləri
- Login səhifəsinə SSO düymələrinin əlavə edilməsi.
- Profil / Tənzimləmələr bölməsində "Developer Settings" -> "API Keys" interfeysi.

## 17. Test ssenariləri
- OAuth2 Refresh Token məntiqinin yoxlanması.
- SSO JIT (Just-In-Time) yaradılmasının test edilməsi (Sistemdə olmayan yeni istifadəçi SSO etdikdə avtomatik yaranırmı).

## 18. Acceptance Criteria
- Təşkilat işçiləri Microsoft/Google hesabları ilə bir kliklə platformaya daxil ola bilməlidir.
- Digər daxili sistemlər Q360-a müraciət etmək üçün müddətli (məs: 1 illik) API Key yarada və istifadə edə bilməlidir.

## 19. AI Development Tasks (Mərhələli Tətbiq Planı - ~35 Tapşırıq)

1. `apps/identity_management` app-ni yarat.
2. `django-oauth-toolkit`, `Authlib` və ya OIDC kitabxanalarını əlavə et.
3. API Key modelini yarat (prefix, hashed_key, revokation_date, user).
4. SSO Provider konfiqurasiyası üçün model yarat.
5. Admin paneldə modelləri qeyd et.
6. OAuth2 urls.py faylını layihənin routing sisteminə əlavə et.
7. OIDC Login endpointini yaz (`/login/microsoft/`).
8. OIDC Callback endpointini yaz. Burada xaricdən gələn JWT-ni decode edib təsdiqləyən funksiya (`Authlib` istifadə edərək).
9. JIT (Just-in-time) Provisioning yaz: Gələn email sistemdə yoxdursa, avtomatik istifadəçi yarat və ona Default Rollar ver.
10. `ApiKeyService.generate_key()` yaz (prefix.secret formatında qaytarsın, lakin bazada ancaq secretin hashini saxlasın).
11. API Key idarəetməsi üçün CRUD endpointləri yarat.
12. Custom Authentication Backend (və ya DRF Authentication class): `ApiKeyAuthentication` yarat. Bu class gələn `Authorization: Api-Key <token>` header-ini oxumalı və cache/DB ilə yoxlamalıdır.
13. Redis Caching: Keçərli API Key-ləri yaddaşda saxlamaq üçün konfiqurasiya.
14. Rol/Scope uyğunlaşdırılması: Xarici SSO-dan gələn qrupları (AD Groups) Q360 daxilindəki RBAC rollarına mappinq edən funksiya yaz.
15. Celery Task: Müddəti bitmiş API keyləri avtomatik disable edən script.
16. Swagger-də API Key və OAuth2 autentifikasiya metodlarını elan et.
17. Integration Test: API Key generasiyası və API çağırma cəhdi.
18. Integration Test: Yanlış API Key ilə sistemə girmə cəhdi (401 Unauthorized).
19. SSO Callback Test: Saxta OIDC token göndərərək xəta mesajının yoxlanması.
20. Məlumatın Təhlükəsizliyi: DB-də Hash funksiyası olaraq PBKDF2 və ya Argon2 təyinatı.

## 20. Risklər
- **Vendor Lock-in/SAML Mürəkkəbliyi:** Bəzi təşkilatlar köhnə SAML2.0 istifadə edə bilər. İlkin versiyada OIDC (OpenID Connect) dəstəyi ilə başlanması, daha sonra ehtiyac olarsa SAML əlavə edilməsi tövsiyə olunur.

## 21. Prioritet
- **Orta (P2)**: Ancaq müştəri / təşkilat tələb etdikdə və B2B inteqrasiyalar başlandıqda aktivləşdirilməlidir. İlkin daxili testlər üçün username/password (JWT) kifayətdir.
