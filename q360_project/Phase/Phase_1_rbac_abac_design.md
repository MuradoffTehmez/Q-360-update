# Phase 1 - RBAC + ABAC Design & Architecture

## 1. Məqsəd
Sistemin icazə və səlahiyyət (Authorization) strukturunu yenidən quraraq həm Rol əsaslı (Role-Based Access Control - RBAC), həm də Atribut/Qayda əsaslı (Attribute-Based Access Control - ABAC) giriş nəzarəti mexanizmini tətbiq etmək.

## 2. Biznes məqsədi
Hazırkı sistemdə olan sərt (hardcoded) icazə məntiqini daha çevik hala gətirmək. Məsələn, "İstifadəçi yalnız özünə aid qeydləri görə bilər" (ABAC) və ya "Yalnız HR Manager rolu olanlar işə qəbul başlada bilər" (RBAC) kimi məntiqləri vahid, dinamik idarəedilən bir siyasət mühərriyinə (Policy Engine) bağlamaq.

## 3. Arxitektura
- **Policy Enforcement Point (PEP) / Policy Decision Point (PDP):** Səlahiyyət yoxlamaları (PEP) API və UI səviyyəsində olacaq, qərarların verilməsi (PDP) isə RBAC/ABAC mühərriki daxilində yerinə yetiriləcək.
- **Django Guard:** Təməl rol idarəetməsi üçün `django.contrib.auth` qrupları və `django-guardian` və ya custom OSL (Object-level Security) istifadə ediləcək, lakin məntiq daha geniş miqyaslı custom service layer üzərində qurulacaq.

## 4. Modul strukturu
```text
q360_project/apps/access_control/
├── models/
├── services/
├── api/
│   ├── serializers/
│   └── views/
├── middlewares/
├── rules_engine/ (ABAC üçün)
└── tests/
```

## 5. Database dəyişiklikləri
### Yeni cədvəllər
- `role` (Rol adları: HR Manager, Developer, s.)
- `permission` (İcazələr: `user.create`, `invoice.view`)
- `role_permission` (Rollar və icazələrin əlaqəsi)
- `user_role` (İstifadəçi və rolun əlaqəsi)
- `abac_policy` (Dinamik qaydalar, JSON formatında)

### Əlaqələr və Constraints
- Rollar arasında İyerarxiya (`parent_role`).
- *Cache*: Rollar və onlara aid olan policy-lər Redis-də in-memory saxlanılacaq.

## 6. API dəyişiklikləri
- **Yeni endpointlər:**
  - `GET /api/v1/roles/`
  - `POST /api/v1/roles/`
  - `POST /api/v1/roles/{id}/permissions/` (Rola icazə bağlamaq)
  - `POST /api/v1/users/{id}/roles/` (İstifadəçiyə rol vermək)
  - `POST /api/v1/policies/` (ABAC Qaydası yaratmaq)
  - `POST /api/v1/auth/check/` (İcazəni yoxlamaq üçün test endpoint-i)

## 7. Servislər (Service Layer)
- `RoleService`: Rol və istifadəçi əlaqələrini idarə edir.
- `PermissionService`: Sistemin bütün endpoint və dataları üzərində CRUD icazələrini oxuyur.
- `AbacEvaluationService`: Soruşulan obyektin atributlarını yoxlayaraq qərar verir (məsələn: `request.user.department_id == resource.department_id`).

## 8. Permission modeli
- **RBAC:** İstifadəçi -> Rol -> Permission.
- **ABAC:** İstifadəçi (Subject), Obyekt (Resource), Fəaliyyət (Action), və Şərtlər (Environment). (Məsələn: Action="Read", Resource="Document", Condition="is_owner=True" or "department=IT").

## 9. Workflow
Bir istifadəçi endpoint-ə (və ya UI komponentinə) müraciət etdikdə, middleware əvvəlcə RBAC (statik icazə) yoxlayır, sonra isə obyekt səviyyəsində ABAC (dinamik icazə) yoxlayır. Əgər hər ikisi `True` qaytararsa, əməliyyat icra edilir.

## 10. Event-lər
- `RoleAssigned`
- `RoleRevoked`
- `PolicyUpdated`

## 11. Security
- İcazə idarəetmə panelinə yalnız `SuperAdmin` və ya `SecurityAdmin` rolu daxil ola bilər.
- Privilege Escalation (Səlahiyyətin qanunsuz artırılması) hücumlarının qarşısını almaq üçün rolların mənimsənilməsi loqlanacaq.

## 12. Logging
- Bütün icazə rəddləri (Access Denied / 403) `security_log` cədvəlində loqlanacaq.

## 13. Audit
- Kimin hansı rolu kimə və nə vaxt verməsi Audit cədvəlinə yazılacaq (Kim: Admin, Nə: Verildi "Maliyyə Müdiri" rolu, Kimə: "Təhməz", Nə vaxt: 2026-07-13).

## 14. Performance
- Obyekt səviyyəsində (Row-level) təhlükəsizlik böyük cədvəllərdə sorğuları zəiflədir. Optimizasiya üçün Policy qaydaları Django ORM `Q` obyektlərinə çevrilərək DB sorğularına inject ediləcək (Filtering at DB level).

## 15. Cache
- Hər request-də istifadəçinin rollarını və RBAC icazələrini DB-dən oxumamaq üçün JWT tokenin içinə və ya Redis sessiyasına yazılacaq. Təzələnmə (Cache invalidation) yalnız rol dəyişdikdə baş verəcək.

## 16. Background process
- Task: Expired olan müvəqqəti rolların (Temporary Access) silinməsi.

## 17. Notification inteqrasiyası
- Kritik rollar (məs: Admin) kiməsə verildikdə təşkilatın Security qrupuna e-mail/Slack bildirişi gedəcək.

## 18. UI dəyişiklikləri
- Role Management Dashboard.
- Policy Builder (Şərtləri qurmaq üçün məntiq interfeysi - "AND", "OR").

## 19. Test ssenariləri
- Rol İyerarxiyası Testi: Parent rolun Child rolunun icazələrini avtomatik miras alması.
- ABAC Testi: Fərqli departamentdən olan işçinin sənədi oxumağa cəhd etməsi və 403 alması.

## 20. Acceptance Criteria
- Hər hansı bir istifadəçiyə eyni anda bir neçə rol verilə bilər.
- Siyasət mühərriki istənilən model obyektinin atributunu oxuyub müqayisə edə bilməlidir.
- API cavab müddəti (icazə yoxlaması daxil) əlavə 20ms-dən çox olmamalıdır.

## 21. AI Development Tasks (Mərhələli Tətbiq Planı - ~40 Tapşırıq)

1. `apps/access_control` app-ni yarat.
2. Abstract və Timestamped model quraşdırmasını et.
3. `Role` modelini yarat.
4. `Permission` modelini (və ya Django `ContentType` əlaqəsini) yarat.
5. `RolePermission` və `UserRole` cədvəllərini yarat.
6. `AbacPolicy` modelini JSONField dəstəyi ilə yarat.
7. Admin paneldə rolların qeydiyyatı.
8. `makemigrations` və `migrate` icra et.
9. JWT token daxilinə `roles` siyahısını əlavə etmək üçün Custom Token serializer yaz.
10. `Role` CRUD üçün API endpointləri və serializerləri yarat.
11. İstifadəçiyə rol atamaq və silmək üçün API yaz.
12. `AbacPolicy` CRUD API-lərini yaz.
13. Django Middleware yarat: `RbacMiddleware` (Endpoint səviyyəsində qoruma).
14. Custom DRF Permission class yarat: `IsRbacAuthorized`.
15. Custom DRF Permission class yarat: `IsAbacAuthorized` (Obyekt səviyyəsində).
16. `AbacEvaluationService` sinfini yaz. (JSON qaydaları parse etməli və obyektlə müqayisə etməlidir).
17. ABAC siyasətlərini Django ORM `Q` filtrlərinə çevirən (Compiler) funksiya yaz.
18. Redis in-memory cache konfiqurasiyası: İstifadəçi rolları üçün `set`, `get`, `invalidate` funksiyaları.
19. SuperAdmin-in bütün yoxlamalardan yan keçməsini (Bypass) təmin edən qısa yol (short-circuit) yaz.
20. `RoleAssigned` və `RoleRevoked` siqnallarını yaz.
21. Cache-i invalidate etmək üçün siqnallara receiver-lər bağla.
22. UI üçün istifadəçinin bütün icazələrini (Flat list) qaytaran `/api/v1/auth/me/permissions/` endpointi yaz.
23. Gələcək müddət üçün rol ataması (Məs: Gələn həftədən etibarən Manager olacaq) dəstəyi (Valid_from, Valid_to).
24. Celery Task: Müddəti bitmiş rolların təmizlənməsi `cleanup_expired_roles()`.
25. Security Auditing üçün Rol dəyişikliklərini `security_log` cədvəlinə yazan servis.
26. Mühüm rola mənimsədilmə zamanı Alert/Notification servisi.
27. N+1 optimizasiyası: İstifadəçini çağırarkən `prefetch_related('roles__permissions')` əlavə et.
28. Unit Test: Rol atama və silmə.
29. Unit Test: Miras alınan rolların icazələrinin hesablanması.
30. Unit Test: ABAC JSON engine testləri (int, str, bool müqayisələri).
31. Integration Test: Səlahiyyətsiz GET request (403 Forbidden).
32. Integration Test: Səlahiyyətsiz POST request (403 Forbidden).
33. Obyekt səviyyəsində ABAC filtr testləri (İstifadəçinin ancaq öz obyektlərini listələməsi).
34. Məlumat bazası indexlərini (Role adı üzrə unique, UserRole üzrə composite index) tətbiq et.
35. Rol silindikdə `UserRole` cədvəlindən kaskad (və ya soft delete) silinməsini konfiqurasiya et.
36. Bütün mövcud Django endpointlərinə DRF Permission klasslarının tətbiqi (Refactoring Phase).
37. Sənədləşmə: Swagger-də Security Definition əlavə et.
38. Caching üçün stress test yaz (Redis response time).
39. Development zamanı default rolları seed etmək üçün Management Command yaz (`python manage.py seed_roles`).
40. Deployment hazırliğı və yoxlamalar.

## 22. Risklər
- Obyekt səviyyəsində edilən (ABAC) xətalar istifadəçilərin vacib məlumatları görməməsinə və ya əksinə sızmasına (Data Leakage) səbəb ola bilər. Qaydalar çox diqqətlə test edilməlidir.
- Cache invalidation problemləri (rol silinir amma cache qaldığı üçün istifadəçi hələ də giriş edə bilir).

## 23. Prioritet
- **Kritik (P0)**: Bütün məlumat təhlükəsizliyi bunun üzərində qurulacaq. Platform Refactoring fazasından dərhal sonra (və ya bərabər) başlanmalıdır.
