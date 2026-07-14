# Phase 1 - Feature Flags Design & Architecture

## 1. Məqsəd
Sistemə əlavə edilən yeni funksiyaların (features) aktiv və ya passiv edilməsini kodda dəyişiklik etmədən, canlı mühitdə (runtime) və müəyyən auditoriya (user, department) üzrə idarə etmək.

## 2. Biznes məqsədi
"Canary Release", "A/B Testing" və "Dark Launching" kimi metodologiyaları təmin etmək. Yeni bir HR modulunu yalnız IT departamenti üçün aktiv edib sınaqdan keçirmək, xəta olduqda tək bir düymə ilə (rollback ehtiyacı olmadan) həmin funksiyanı söndürmək.

## 3. Arxitektura
- **Micro-kernel / Toggling Architecture:** Modul sadə bir if-else strukturundan ibarət olsa da, performansı yüksək tutmaq üçün məlumatlar tamamilə RAM/Cache (Redis) üzərindən idarə ediləcək.
- Django xaricində Front-end-ə (Vue/React) feature-lərin vəziyyətini bildirmək üçün xüsusi API olacaqdır.

## 4. Modul strukturu
```text
q360_project/apps/feature_flags/
├── models/
├── services/
├── api/
│   ├── serializers/
│   └── views/
├── utils/ (Decorators, Context processors)
└── tests/
```

## 5. Database dəyişiklikləri
### Yeni cədvəllər
- `feature_flag` (Adı, Statusu: Aktiv/Deaktiv)
- `feature_flag_rule` (Hansı hallarda aktivdir? - Məs: UserID=5 və ya Department=IT)
- `feature_flag_history` (Dəyişiklik logları)

### Əlaqələr və Constraints
- `feature_flag_rule` cədvəli `feature_flag`-a bağlıdır.

## 6. API dəyişiklikləri
- **Yeni endpointlər:**
  - `GET /api/v1/features/` (CRUD idarəetməsi üçün)
  - `POST /api/v1/features/`
  - `GET /api/v1/features/client/` (UI-ın yalnız özünə aid olan aktiv flagları alması üçün public/authenticated endpoint)
  - `POST /api/v1/features/{id}/toggle/` (Aktivləşdir / Deaktivləşdir)

## 7. Servislər (Service Layer)
- `FeatureFlagManager`: Flag-ın cari statusunu qiymətləndirən məntiq (`is_enabled(feature_name, context)`).
- `FlagCacheService`: Flag məlumatlarını Redis ilə sinxron saxlayan servis.

## 8. Permission modeli
- Yalnız `System Admin` və `Product Manager` rolları fərqli feature flag-ləri idarə edə bilər.
- `client/` API-ni çağıran istifadəçinin öz tokeni/contexti istifadə edilərək yalnız ona görünə bilən funksiyalar qaytarılır.

## 9. Workflow
Feature flag birbaşa heç bir workflow başlatmır. Lakin digər app-lər daxilində `@feature_enabled('new_ui')` kimi dekoratorlar vasitəsilə müraciət qəbul edir.

## 10. Event-lər
- `FeatureToggled` (Bir funksiya aktiv və ya passiv edildikdə)

## 11. Security
- "Fail-close" məntiqi: Əgər Feature Flag servisi cavab verməzsə (məs: Redis çöküb), defolt olaraq yeni funksiyalar sönülü (`False`) hesab edilir ki, qorunmayan və ya natamam kod üzə çıxmasın.

## 12. Logging
- Hansı flag-ın kim tərəfindən dəyişdirildiyi loglanacaq.

## 13. Audit
- Təsadüfən bütün müştərilər üçün test modulu açılmasın deyə Audit log yazılacaq.

## 14. Performance
- Bu modul sistemin hər nöqtəsində (hər view, hər API call) işə düşə bilər. DB sorğusu QƏTİYYƏN olmamalıdır. Məlumatlar yalnız Redis və ya in-memory lokal (LRU cache) yaddaşda oxunmalıdır. API cavab müddəti < 1ms olmalıdır.

## 15. Cache
- Bütün feature və qayda məlumatları Hash map şəklində Redis-də oturacaq.

## 16. Background process
- Periodik sinxronizasiya (Redis və DB arasında uyğunsuzluq olarsa, məs: Redis restart olsa DB-dən geri yükləmə taskı).

## 17. Notification inteqrasiyası
- Vacib bir feature söndürüldükdə DevOps komandasına Telegram/Slack bildirişi (Feature X was emergency disabled).

## 18. UI dəyişiklikləri
- Admin paneldə On/Off switch-ləri (Toggle düymələri).
- Qaydalar qurmaq (Məs: 10% istifadəçi üçün aç) üçün bölmə.

## 19. Test ssenariləri
- Qismən Rollout Testi: 10% istifadəçi qaydasının düzgünlüyünün (hash ilə yoxlanması) test edilməsi.
- Cache sıradan çıxdıqda Fail-close davranışının test edilməsi.

## 20. Acceptance Criteria
- Yeni funksiya saniyələr içində canlı mühitdə aktiv və ya passiv edilə bilməlidir.
- Performansa mənfi təsiri (DB hit) olmamalıdır.
- Funksiyanı yalnız seçilmiş departamentə/istifadəçiyə açmaq mümkün olmalıdır.

## 21. AI Development Tasks (Mərhələli Tətbiq Planı - ~30 Tapşırıq)

1. `apps/feature_flags` app-ni yarat.
2. `FeatureFlag` modelini qur (Name, is_active flag).
3. `FeatureFlagRule` modelini qur (Condition JSON).
4. `FeatureFlagHistory` modelini qur.
5. Admin qeydiyyatı və Miqrasiyalar.
6. DB dəyişikliklərini Redis-ə push edəcək `save()` override yaz və ya signal tətbiq et.
7. `FeatureFlagSerializer` və `FeatureFlagRuleSerializer` yarat.
8. Admin API ViewSet yarat: `FeatureFlagViewSet`.
9. `POST /toggle/` endpointini yaz.
10. `FeatureFlagManager.is_enabled(flag_name, user_context)` funksiyasını in-memory (Redis) axtarışı ilə yaz.
11. İstifadəçinin ID-si və ya xüsusiyyətinə əsasən %-lik rollout (məs: yalnız 10% user görsün) edəcək Hashing məntiqini yaz (Məs: `hash(user_id) % 100 < 10`).
12. Client/UI tərəfin çağıracağı, istifadəçiyə uyğun bütün aktiv flagları (dictionary kimi) qaytaran API yaz.
13. View-ları və API endpointləri qorumaq üçün `@feature_required('flag_name')` dekoratorunu yarat.
14. DRF üçün xüsusi Permission Class: `FeatureFlagPermission`.
15. Django Templates üçün Context Processor əlavə et (əgər hələ də istifadə edilirsə) `{{ features.new_dashboard }}`.
16. Celery Task: Redis çöküb qalxdıqda DB-dən datanı Redis-ə dolduran init_task `sync_feature_flags()`.
17. Redis əlçatmaz olduqda `Fail-safe` / `Fail-close` (False qaytarmaq) catch bloku.
18. `FeatureToggled` siqnalı və audit loglama mexanizmi.
19. Notification: Kritik bir flag söndürüldükdə Slack hook çağırışı.
20. Unit Test: Bütün flag passivdirsə funksiya False qaytarır.
21. Unit Test: Flag yalnız `user_id=1` üçün aktivdirsə yoxlama.
22. Unit Test: 50% rollout logic hash testləri.
23. Unit Test: Dekoratorun 404 (və ya 403) qaytarması, əgər flag sönülüdürsə.
24. Integration Test: Toggle API-nin işləməsi və dərhal nəticə verməsi (Redis sinxron).
25. Security: Rollout qaydalarına təsdiqlənməmiş (unauthenticated) istifadəçilərin konteksti düşdükdə crash olmama testləri (AnonymousUser handling).
26. Management command: `python manage.py load_default_flags` (Yenidən qurulma zamanı standart flag-lərin DB-yə əlavəsi).
27. Sənədləşmə: Developer-lər üçün "Yeni funksiya yazarkən flag-dan necə istifadə etməli" bələdçisi (Markdown).
28. Swagger Documentation Update.
29. Caching stress testi yazılması.

## 22. Risklər
- **Texniki Borc (Technical Debt):** Feature flag-lər kodun içində çoxlu `if-else` yaradır. Köhnəlmiş və daimi açıq qalan flag-lərin mütəmadi koddan silinməsi lazımdır.
- Redis dayandıqda bütün yeni funksiyaların bağlanması.

## 23. Prioritet
- **Aşağı-Orta (P2/P3)**: İlk mərhələdə məcburi deyil, lakin CI/CD və Agile deployment mədəniyyətini qurmaq üçün vacibdir.
