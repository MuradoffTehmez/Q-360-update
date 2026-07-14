# Phase 1 - Workflow Engine Design & Architecture

## 1. Məqsəd
Təşkilat daxilində bütün mürəkkəb təsdiq proseslərinin (məsələn, məzuniyyət, xərc, satınalma tələbləri, işəqəbul və s.) avtomatlaşdırılması, izlənməsi və mərkəzi bir mühərrik (engine) tərəfindən idarə edilməsi.

## 2. Biznes məqsədi
Sistemdə mövcud olan *hardcoded* (kodlaşdırılmış) təsdiq məntiqlərinin çıxarılması və vizual, dinamik, konfiqurasiya edilə bilən iş axını sisteminin qurulması. Təsdiq sürətinin artırılması, proseslərin şəffaflığı və hesabatlılığın təmin edilməsi.

## 3. Mövcud vəziyyət (Q360-da hazırda nə var)
- Workflow modulu yoxdur.
- Məlumatlar *manual approve* (əllə təsdiq) edilir.
- *State Machine* (Vəziyyət maşını) məntiqi mövcud deyil, hər modul öz state-lərini saxlayır.
- *Approval Chain* (Təsdiq zənciri) statikdir.
- *Escalation* (Eskalasiya/Yuxarı pilləyə keçid) mexanizmi yoxdur.
- *Parallel Approval* (Paralel təsdiqləmə) imkanı yoxdur.

## 4. Arxitektura
- **Microservice / Modular Monolith Pattern:** Workflow Engine, Q360-in əsas app-lərindən ayrı bir Django `apps/workflow_engine` modulu (və ya gələcək üçün ayrı mikroservis) olaraq dizayn ediləcək.
- **Event-Driven Architecture (EDA):** Təsdiq prosesindəki vəziyyət dəyişiklikləri event-lər (siqnallar və message broker - Celery/RabbitMQ) vasitəsilə digər modullara ötürüləcək.
- **State Machine Integration:** Hər bir workflow `django-fsm` və ya custom state manager ilə idarə olunacaq.

## 5. Modul strukturu
```text
q360_project/apps/workflow_engine/
├── models/
├── services/
├── api/
│   ├── serializers/
│   └── views/
├── events/
├── tasks/
├── rules_engine/
└── tests/
```

## 6. Database dəyişiklikləri
### Yeni cədvəllər
- `workflow_template` (Workflow strukturu)
- `workflow_step` (Hər mərhələ)
- `workflow_transition` (Mərhələlər arası keçid)
- `workflow_condition` (Keçid üçün qaydalar)
- `workflow_instance` (İşləyən aktiv workflow - Request)
- `workflow_instance_step` (Aktiv workflow-nun cari mərhələsi)
- `workflow_history` (Audit log üçün tarixçə)
- `approval_action` (Təsdiq / Rədd əməliyyatları)

### Əlaqələr və Constraints
- `workflow_instance` -> `workflow_template` (Foreign Key)
- *Unique Constraint*: Birlikdə `(instance_id, step_id, status)` unikallığı.
- *Index*: `status`, `assigned_to`, `created_at` sahələrində axtarış sürəti üçün.
- *Soft Delete*: Silinməsi əvəzinə `is_deleted=True` istifadəsi.

## 7. API dəyişiklikləri
- **Yeni endpointlər:**
  - `POST /api/v1/workflow/templates/` (Yeni workflow yarat)
  - `POST /api/v1/workflow/instances/` (Workflow başlat)
  - `POST /api/v1/workflow/instances/{id}/approve/` (Təsdiqlə)
  - `POST /api/v1/workflow/instances/{id}/reject/` (Rədd et)
  - `GET /api/v1/workflow/instances/pending/` (İstifadəçini gözləyən təsdiqlər)
- **Pagination & Filtering:** Bütün list API-lərdə aktiv olacaq.
- **Validation:** DRF validatorları və ya Pydantic.

## 8. Servislər (Service Layer)
- `WorkflowService`: Workflow yaratmaq və state dəyişmək.
- `TransitionService`: Bir state-dən digərinə keçid məntiqi.
- `ApprovalService`: İstifadəçi təsdiqləri və hüquq yoxlaması.
- `HistoryService`: Tarixçənin yazılması.
- `NotificationService`: Əlaqədar şəxslərə email/push göndərilməsi.
- `RuleEngine / ConditionEngine`: Təsdiqin növbəti mərhələyə keçib-keçməməsi üçün dinamik qaydaların (məs: "Məbləğ > 1000") yoxlanılması.

## 9. Permission modeli (RBAC + ABAC)
- **RBAC:** İstifadəçinin Təsdiqetmə rolu olmalıdır (məs. `Department Manager`).
- **ABAC:** İstifadəçi yalnız öz departamentinin və ya asılılığında olan şəxslərin sorğusunu təsdiqləyə bilər.
- **Dynamic Permission:** `Department`, `Position`, `Manager Hierarchy` əsasında təyin ediləcək.

## 10. Event-lər
- `WorkflowStarted`
- `WorkflowStepCompleted`
- `WorkflowCompleted`
- `WorkflowRejected`
- `WorkflowCancelled`
- `WorkflowEscalated`
- `WorkflowExpired`

## 11. Security
- Endpointlər OAuth2/JWT vasitəsilə qorunacaq.
- IDOR (Insecure Direct Object Reference) hücumlarının qarşısını almaq üçün təsdiqləyənin həqiqətən təsdiq hüququ olması mütləq yoxlanılacaq.

## 12. Logging & Audit
- **Business Log:** Kim nəyi təsdiqlədi, nə vaxt.
- **Security Log:** İcazəsiz təsdiq cəhdləri.
- **Audit Log:** Workflow qaydalarının (Template) dəyişdirilməsi tarixçəsi.

## 13. Performance & Cache
- **Caching:** Workflow Template-lər (çox dəyişmədikləri üçün) Redis-də cache-lənəcək.
- **Indexes:** Pending tasks (Gözləyən tapşırıqlar) sorğularını sürətləndirmək üçün kompozit indexlər yaradılacaq.
- **Query Optimization:** N+1 query problemlərinin (məs. `select_related`, `prefetch_related`) həlli.

## 14. Background process
- **Celery Tasks:** Escalation, Timeout və Reminder prosesləri arxa fonda asinxron işləyəcək.

## 15. Notification inteqrasiyası
- **Email, SMS, Push, Webhook, MS Teams, Slack.**
- **Scheduler:** 
  - *Reminder*: Təsdiq gözləyəndə gündəlik xatırlatma.
  - *Escalation*: Təsdiq 3 gün ərzində edilməzsə, bir üst rəhbərə eskalasiya.

## 16. UI dəyişiklikləri
- Visual Workflow Builder (Drag & Drop interfeysi - Vue/React və ya JS libs).
- Təsdiqlər qutusu (My Approvals Dashboard).
- Request izləmə xətti (Timeline).

## 17. Test ssenariləri
- Unit Testlər (Modeller və Servislər üçün).
- Integration Testlər (API endpointlər, State keçidləri).
- Load Testing (Eyni anda 1000 təsdiq prosesinin başladılması).

## 18. Acceptance Criteria (Qəbul Şərtləri)
- İstifadəçi UI üzərindən tam fərdi workflow qura bilməlidir.
- Şərtləndirilmiş (Conditional) təsdiqlər (Məs: Xərc > 100 AZN olduqda CEO təsdiqi tələb olunur) işləməlidir.
- Bütün transition-lar (keçidlər) `workflow_history` cədvəlində öz əksini tapmalıdır.
- Eskalasiya müddəti bitdikdə, sistem avtomatik bildiriş göndərməlidir və statusu dəyişməlidir.
- Bütün testlər (Coverage > 85%) uğurla keçməlidir.

## 19. AI Development Tasks (Mərhələli Tətbiq Planı - ~50 Tapşırıq)

Aşağıdakı siyahı AI Agent (və ya Developer) tərəfindən ardıcıl icra edilmək üçün nəzərdə tutulmuşdur:

### Quraşdırma və Konfiqurasiya (Tasks 1-5)
1. Yeni `workflow_engine` Django app-ni yarat.
2. `settings.py` faylına `workflow_engine` app-ni əlavə et.
3. Təməl qovluq strukturunu (`services/`, `events/`, `rules_engine/`) qur.
4. `celery` quraşdırmasının aktivliyini yoxla və `workflow_engine/tasks.py` faylını yarat.
5. Yeni modul üçün test mühitinin (pytest) izolasiyasını konfiqurasiya et.

### Verilənlər Bazası və Modellər (Tasks 6-15)
6. Abstract Model (TimeStamped, SoftDeletable) yarat.
7. `WorkflowTemplate` modelini yarat.
8. `WorkflowStep` modelini yarat (Template ilə əlaqəli).
9. `WorkflowTransition` modelini yarat (Source Step, Destination Step).
10. `WorkflowCondition` modelini yarat (JSON field olaraq Rule saxlanacaq).
11. `WorkflowInstance` modelini yarat (Content Type / Generic ForeignKey ilə digər app-lərə bağlana bilməsi üçün).
12. `WorkflowInstanceStep` modelini yarat.
13. `ApprovalAction` və `WorkflowHistory` modellərini yarat.
14. Django admin paneli üçün bütün bu modelləri qeydiyyatdan keçir (`admin.py`).
15. Makemigrations və migrate əməliyyatlarını həyata keçir.

### API Layer - Serializers & Views (Tasks 16-25)
16. `WorkflowTemplate` üçün CRUD serializer-ləri yarat.
17. `WorkflowStep` və `Transition` üçün nested serializer-lər yarat.
18. `WorkflowTemplateViewSet` yarat və router-ə əlavə et.
19. `WorkflowInstanceSerializer` yarat (Read və Write üçün ayrı-ayrı).
20. `WorkflowInstanceViewSet` yarat.
21. İstifadəçini gözləyən tapşırıqlar (Pending Approvals) üçün custom endpoint (`@action`) yarat.
22. Action endpoint-i yarat: `Approve` (Təsdiqlə).
23. Action endpoint-i yarat: `Reject` (Rədd et).
24. Action endpoint-i yarat: `Cancel` (Sorğu sahibi tərəfindən ləğv).
25. API sənədləşməsini (Swagger/OpenAPI schema) yenilə.

### Service Layer və Business Logic (Tasks 26-35)
26. `WorkflowService.create_template()` metodunu yaz.
27. `WorkflowService.start_instance()` metodunu yaz.
28. `RuleEngine.evaluate_conditions()` metodunu yaz (JSON məntiqini parse edən).
29. `TransitionService.get_next_step()` metodunu yaz.
30. `ApprovalService.approve_step()` məntiqini yaz (İcazə yoxlaması ilə birlikdə).
31. `ApprovalService.reject_step()` məntiqini yaz.
32. Parallel təsdiq yoxlaması: Bütün parallel iştirakçılar təsdiq etmədən növbəti mərhələyə keçidi əngəlləyən funksiyanı yaz.
33. `HistoryService.log_action()` metodunu hər tranzaksiyada işə düşəcək şəkildə inteqrasiya et.
34. ContentType köməyilə istənilən obyektin statusunu avtomatik dəyişəcək webhook məntiqini yaz.
35. `NotificationService.send_approval_notification()` xidmətini qur.

### Background Tasks, Eventlər və Schedulers (Tasks 36-40)
36. Django siqnalları və ya xüsusi Event sistemi qur (`WorkflowStarted`, `WorkflowCompleted`).
37. Celery Task: `check_expired_workflows()` yarat.
38. Celery Task: `escalate_pending_approvals()` yarat.
39. Celery Task: `send_reminder_emails()` yarat.
40. Celery Beat schedule-ə reminder və eskalasiya tasklarını əlavə et.

### Security, Validation və Performance (Tasks 41-45)
41. RBAC/ABAC middleware/permission class-ı yaz (`IsApproverPermission`).
42. Xüsusi validasiya: Workflow template-də circular (dairəvi) transition-ların (sonsuz döngə) qarşısını almaq üçün validator yaz.
43. N+1 problemi üçün Serializer-lərdə və ViewSet queryset-lərində `select_related` və `prefetch_related` əlavə et.
44. Template-lər üçün Redis cache tətbiq et.
45. Verilənlər bazasında `WorkflowInstance.status` və `assigned_to` üzrə Index yarat.

### Test Ssenariləri (Tasks 46-52)
46. Model Unit Testləri: Bütün modellərin yaranması və string representasiyaları.
47. Service Unit Testləri: `RuleEngine` üçün fərqli operatorların test edilməsi.
48. API Integration Testləri: Template yaratma və listələmə API-lərinin testi.
49. API Integration Testləri: Workflow başlatma və Approve/Reject cycle-nın test edilməsi.
50. Permission Testləri: Səlahiyyəti olmayan istifadəçinin təsdiq cəhdini test et.
51. Celery Task Testləri: Eskalasiya vaxtı bitdikdə düzgün step-ə keçid.
52. Data Consistency Testi: Race Condition qarşısını alan lock mexanizmini test et.

## 20. Risklər
- **Race Conditions:** Eyni anda iki istifadəçi eyni iş axınını təsdiq etməyə çalışarsa database inconsistency ola bilər (Pessimistic or Optimistic Locking tətbiq olunmalıdır).
- **Mürəkkəblik:** Mürəkkəb (və çoxşaxəli) qaydaların icrası zamanı rule engine-də xətaların baş verməsi.
- **Performans Dropu:** Çox sayda gözləyən history log-ların DB-ni yavaşlatması (Archive mexanizmi qurulmalıdır).

## 21. Prioritet
- **Kritik (P0)**: Q360-da bütün əsas modulların (HR, Finans, Satınalma) gələcəyi bu modula bağlıdır. İlk olaraq Workflow Engine canlıya alınmalıdır.
