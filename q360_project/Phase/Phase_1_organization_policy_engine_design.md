# Phase 1 - Organization Policy Engine Design & Architecture

## 1. Məqsəd
Təşkilatın daxili siyasətlərinin (HR qaydaları, xərc limitləri, iş saatları, məzuniyyət günlərinin hesablanması, overtime tələbləri və s.) kod daxilindən (hardcoded) çıxarılaraq vizual və ya qayda (rule) əsaslı sistem üzərindən idarə edilməsi.

## 2. Biznes məqsədi
Sistem administratorlarına (və ya HR/Maliyyə menecerlərinə) developerlərə ehtiyac duymadan biznes qaydalarını dəyişməyə imkan yaratmaq. Məsələn: "Əgər işçinin stajı > 5 ildirsə, illik məzuniyyəti 30 gündür, əks halda 21 gündür." kimi qaydaları asanlıqla konfiqurasiya etmək.

## 3. Arxitektura
- **Rule Engine Architecture:** Qaydaların idarə edilməsi və dəyərləndirilməsi üçün abstrakt mühərrik (məs. *business-rules* kitabxanası əsasında və ya custom JSON logic evaluator).
- **Service/Domain layer separation:** Tətbiqin digər domenlərinin (HR, Finance) öz daxilində şərtləri yoxlaması əvəzinə `PolicyEngine.evaluate(context)` çağırışı ilə mərkəzi qərar mərkəzindən asılı olması.

## 4. Modul strukturu
```text
q360_project/apps/policy_engine/
├── models/
├── services/
├── api/
│   ├── serializers/
│   └── views/
├── evaluators/
└── tests/
```

## 5. Database dəyişiklikləri
### Yeni cədvəllər
- `policy` (Siyasətin adı və aid olduğu domen. Məs: 'Leave Calculation')
- `policy_rule` (Şərtlər və Hərəkətlər - Conditions & Actions JSON)
- `policy_version` (Qaydaların tarixçəsi və versiyalanması)
- `policy_evaluation_log` (Hansı qayda nə zaman işlədi və nə nəticə verdi - Debug üçün)

### Əlaqələr və Constraints
- Qaydalar versiyalanacaq (Active version flag).
- `policy` -> `policy_rule` (One-to-Many).

## 6. API dəyişiklikləri
- **Yeni endpointlər:**
  - `GET /api/v1/policies/`
  - `POST /api/v1/policies/`
  - `POST /api/v1/policies/evaluate/` (Müəyyən context göndərərək nəticəni almaq)
  - `POST /api/v1/policies/{id}/versions/` (Yeni versiya yaratmaq)
  - `POST /api/v1/policies/{id}/activate/` (Versiyanı aktivləşdirmək)

## 7. Servislər (Service Layer)
- `PolicyManagementService`: Qaydaların yaradılması və versiyalanması.
- `PolicyEvaluationService`: Gələn parametrlərə (Context) əsasən JSON qaydalarını oxuyub riyazi/məntiqi əməliyyat edərək nəticə çıxarmaq.

## 8. Permission modeli
- Yalnız `PolicyManager` rolu siyasətləri yarada və ya dəyişə bilər.
- Adi istifadəçilərin yalnız `evaluate` (avtomatik proseslər vasitəsilə) oxuma izni olacaqdır.

## 9. Workflow
Modul Workflow Engine ilə sıx işləyə bilər. Workflow Condition-lar birbaşa Policy Engine-ə müraciət edərək "Bu təsdiq prosesinə ehtiyac varmı?" sualına cavab ala bilər.

## 10. Event-lər
- `PolicyCreated`
- `PolicyActivated`
- `PolicyFailedToEvaluate` (Şərtlərdə xəta olduqda)

## 11. Security
- Code Injection qarşısını almaq üçün qaydalarda Python funksiyası (eval() / exec()) işlədilməyəcək, yalnız qapalı operatorlar (`>`, `<`, `==`, `in`, `contains`) istifadə ediləcək (AST və ya JSONLogic parser istifadə edilərək).

## 12. Logging
- Bütün Policy dəyişiklikləri audit loqa yazılacaq.
- Şərtlərin pars edilməsindəki səhvlər system log-a "Error" kimi düşəcək.

## 13. Audit
- Köhnə siyasətlərin silinməsi qadağandır (Soft Delete və Versioning var). Çünki keçmişə dönük hesabatlarda "Bu niyə belə hesablanıb?" sualına həmin vaxt aktiv olan siyasət versiyası cavab verəcək.

## 14. Performance
- Siyasətlər dəyərləndirilərkən mürəkkəb regexlər və ya ağır DB sorğuları (Context-i yığmaq üçün) ola bilər. Context toplanması policy xaricində, çağıran tərəfdən edilməlidir.

## 15. Cache
- Aktiv `PolicyRule` obyektləri in-memory (Redis) saxlanılacaq ki, saniyədə yüzlərlə evaluate prosesi DB-ni yormasın.

## 16. Background process
- Qayda dəyişildiyi zaman "Retroactive" (keçmişə tətbiq) funksiyası seçilibsə, Celery Task köhnə dataları yenidən hesablayacaq.

## 17. Notification inteqrasiyası
- Vacib şirkət siyasəti aktivləşdirildikdə (məs. yeni işə çıxma saatı), sistem tərəfindən Slack/Email vasitəsilə elan (Announcement) göndərilməsi.

## 18. UI dəyişiklikləri
- Policy Builder (Condition - Action vizual bloku).
- Version History və Rollback (Geri qaytarma) düyməsi.

## 19. Test ssenariləri
- Ən mürəkkəb biznes ssenarisinin (AND/OR əlaqəli çoxlu şərtlər) test edilməsi.
- Xətalı məlumat tipində (String vs Int) evaluate funksiyasının çökməməsi.

## 20. Acceptance Criteria
- Təşkilat siyasətləri vizual interfeys üzərindən yazılacaq struktura (JSONLogic) çevrilməlidir.
- Versiyalama işləməlidir (köhnə qayda dəyişdirilmir, yenisi yaranır).
- Qərarvermə funksiyası heç bir vəziyyətdə (səhv input verilsə belə) sistemi dayandırmamalı (Exception throw), default fail-safe dəyər qaytarmalıdır.

## 21. AI Development Tasks (Mərhələli Tətbiq Planı - ~35 Tapşırıq)

1. `apps/policy_engine` app-ni yarat.
2. `Policy` və `PolicyRule` modellərini yarat.
3. `PolicyVersion` modelini (Active flag ilə) qur.
4. `PolicyEvaluationLog` modelini qur.
5. Admin paneldə modellərin qeydiyyatı.
6. DB miqrasiyalarını icra et.
7. `PolicyManagementService.create_version()` yaz.
8. `PolicyManagementService.activate_version()` yaz.
9. JSONLogic parse edəcək / evaluate edəcək parser qur (`json_logic` və ya custom engine).
10. `PolicyEvaluationService.evaluate(policy_code, context)` metodunu yaz.
11. Serializer: `PolicySerializer`.
12. Serializer: `PolicyRuleSerializer`.
13. API ViewSet: `PolicyViewSet` yarat.
14. API Endpoint: `POST /evaluate/` (Debug məqsədilə API).
15. API Endpoint: `POST /activate/` action-nı viewset-ə əlavə et.
16. Hər `activate` əməliyyatından əvvəl digər versiyaların aktivliyini ləğv edən funksiya (Unique Active Constraint).
17. Redis cache inteqrasiyası: `get_active_policy(policy_code)`.
18. Cache invalidation məntiqini (activate olduqda) yaz.
19. `PolicyActivated` siqnalı üçün receiver yaz.
20. Celery Task: Keçmiş dataları yenidən hesablamaq (Retroactive Update).
21. Təhlükəsizlik üçün: Input validasiyası (JSON sxeminin düzgünlüyü yoxlanışı).
22. UI üçün available operatorları (`==`, `>=`, `contains`) qaytaran helper endpoint yaz.
23. Gələn `context` datalarının tiplərinin policy-ə uyğun olmasını yoxlayan validation funksiyası.
24. `PolicyEvaluationLog` üçün asynchronous yazma məntiqi (DB I/O zəiflətməmək üçün Celery ilə loqlama).
25. Unit Test: Operatorların yoxlanması (Məs: 5 > 3).
26. Unit Test: İç-içə (Nested) JSON qaydalarının dəyərləndirilməsi.
27. Unit Test: Default return value (Şərtlərin heç biri ödənmədikdə).
28. Integration Test: Tam CRUD və version aktivləşdirmə.
29. Caching Test: Cache-dən oxuma sürəti vs DB-dən oxuma.
30. Təşkilatın ilk 3 default policy-sini sistemə miqrasiya qismində (və ya management command kimi) əlavə et.
31. Permission Class: `IsPolicyAdmin` yalnız onlara dəyişmə haqqı.
32. Sənədləşmə: Siyasət necə yazılır? (Markdown documentation daxildə).
33. API Swagger Doc əlavələri.
34. Backend code-coverage-in 90%-dən yuxarı olduğuna əmin ol.

## 22. Risklər
- Qaydaların qurulmasında biznes məntiqi xətaları (Məs: Operatorun səhv seçilməsi) kritik təşkilati maliyyə xətalarına (səhv bonus hesablanması) gətirib çıxara bilər. Dry-run (Test) imkanı olmalıdır.

## 23. Prioritet
- **Orta-Yüksək (P1/P2)**: HR və Maliyyə modullarının keçidi üçün baza rolunu oynayır. Workflow Engine-dən sonra təqdim oluna bilər.
