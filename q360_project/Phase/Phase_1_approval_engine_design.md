# Phase 1 - Approval Engine Design & Architecture

## 1. Məqsəd
İş axınlarından (Workflow Engine) gələn və ya birbaşa digər modullardan (məs. sənəd təsdiqi) tələb olunan təsdiq əməliyyatlarının mərkəzləşdirilmiş idarəetməsi, təsdiqləmə zəncirlərinin qurulması və icazə səlahiyyətlərinin avtomatlaşdırılması.

## 2. Biznes məqsədi
Müxtəlif departament və modulların ehtiyac duyduğu təsdiq məntiqini tək bir sistemdə cəmləşdirmək. Paralel təsdiqləmələr, avtomatik təsdiqlər, nümayəndə (delegation) təyin edilməsi kimi imkanları təqdim edərək qərarların verilmə sürətini artırmaq.

## 3. Arxitektura
- **Modular Monolith:** Django daxilində `apps/approval_engine` modulu kimi hazırlanacaq. Workflow Engine ilə sıx inteqrasiyada işləyəcək, lakin asılılığı minimuma endirmək üçün interfeyslər (Service-to-Service call) vasitəsilə xəbərləşəcək.
- **Pluggable Approval Strategy:** Fərqli obyektlər üçün (Xərc, İşə qəbul, Tətil) Strategy Pattern istifadə olunacaq.

## 4. Modul strukturu
```text
q360_project/apps/approval_engine/
├── models/
├── services/
├── api/
│   ├── serializers/
│   └── views/
├── strategies/
├── tasks/
└── tests/
```

## 5. Database dəyişiklikləri
### Yeni cədvəllər
- `approval_chain` (Təsdiq zəncirinin növü, ardıcıllığı)
- `approval_node` (Zəncirin hər bir halqası - kim(lər) təsdiqləməlidir)
- `approval_request` (Gözləyən konkret bir təsdiq sorğusu)
- `approval_delegation` (Təsdiq səlahiyyətinin başqasına ötürülməsi/əvəzedici)
- `approval_log` (Tarixçə)

### Əlaqələr və Constraints
- `approval_request` -> `approval_node` və `GenericForeignKey` ilə hədəf obyektə.
- *Index*: `status`, `assigned_user`, `assigned_group` sahələri.

## 6. API dəyişiklikləri
- **Yeni endpointlər:**
  - `POST /api/v1/approvals/chains/` (Zəncir yaratmaq)
  - `GET /api/v1/approvals/requests/pending/` (Mənə aid gözləyən sorğular)
  - `POST /api/v1/approvals/requests/{id}/approve/`
  - `POST /api/v1/approvals/requests/{id}/reject/`
  - `POST /api/v1/approvals/requests/{id}/reassign/` (Başqasına yönləndir)
  - `POST /api/v1/approvals/delegations/` (Məzuniyyətdəyəm, icazəmi filankəsə verirəm)

## 7. Servislər (Service Layer)
- `ApprovalChainService`: Zəncirlərin idarəsi.
- `ApprovalExecutionService`: Təsdiqləmə, rədd etmə məntiqi.
- `DelegationService`: Avtomatik əvəzedicini tapmaq (məs. istifadəçi məzuniyyətdədirsə).
- `EscalationService`: Vaxtı keçmiş təsdiqləri yuxarı instansiyaya ötürmək.

## 8. Permission modeli (RBAC + ABAC)
- **ABAC:** Təsdiq tələb edən obyektin xüsusiyyətlərinə görə icazə.
- **RBAC:** Delegasiya (Əvəzetmə) zamanı, əvəzedicinin kifayət qədər rolu/vəzifəsi olub-olmaması yoxlanılacaq.

## 9. Workflow
Approval Engine Workflow Engine tərəfindən çağırıla bilər. Workflow Step-in növü "Approval" olduqda, bu engine prosesi devralır, zənciri yoxlayır, sonlanan zaman isə `ApprovalCompleted` event-i ataraq Workflow-u davam etdirir.

## 10. Event-lər
- `ApprovalRequested`
- `ApprovalGranted`
- `ApprovalDenied`
- `ApprovalEscalated`
- `DelegationActivated`

## 11. Security
- İkitərəfli doğrulama (Kritik əməliyyatlar üçün MFA və ya PIN kodu istənə bilər).
- CSRF qorunması.
- Rate limiting (Brute-force approve/reject API zənglərinin qarşısını almaq).

## 12. Logging
- Bütün əməliyyatlar `approval_log` cədvəlində IP, User Agent və TimeStamp ilə qeyd olunacaq.

## 13. Audit
- Təsdiq zəncirindəki istənilən konfiqurasiya dəyişikliyi (kiminsə səlahiyyətinin alınması) ciddi Audit Log-da saxlanacaq.

## 14. Performance
- `GenericForeignKey` yavaşlıq yarada bilər, buna görə spesifik cədvəllərlə əlaqələr Materialized View və ya Caching (Redis) ilə optimallaşdırılacaq.

## 15. Cache
- Aktiv Delegation-lar (İstifadəçi A öz icazəsini B-yə verib) Redis-də saxlanılacaq, hər dəfə DB-yə sorğu atılmayacaq.

## 16. Background process
- Celery Task: Eskalasiya vaxtı bitən sorğuların yoxlanılması.
- Celery Task: Delegation vaxtı (məs: Məzuniyyət bitdikdə) bitən qeydlərin ləğvi.

## 17. Notification inteqrasiyası
- Yeni təsdiq sorğusu gəldikdə Push Notification.
- Təsdiq gecikdikdə Email Reminder.

## 18. UI dəyişiklikləri
- Delegation Panel (My Substitutes).
- Gözləyən təsdiqlər widget-ı (Dashboard).

## 19. Test ssenariləri
- Əvəzedici məntiqinin testi (Delegation dövrlərinin kəsişməsi).
- Paralel zəncir testi (3 nəfərdən 2-nin təsdiqi kifayət edərmi - *Quorum* məntiqi).

## 20. Acceptance Criteria
- Təsdiq səlahiyyəti başqasına müvəqqəti verilə bilməlidir.
- Quorum (çoxluq) təsdiq məntiqi (məsələn, 3 nəfərdən 2-si) işləməlidir.
- Şərtləri ödəməyən şəxs təsdiqləmə edə bilməməlidir.

## 21. AI Development Tasks (Mərhələli Tətbiq Planı - ~35 Tapşırıq)

1. `apps/approval_engine` modulu yarat və `settings.py`-a əlavə et.
2. Abstract modelləri yarat.
3. `ApprovalChain` və `ApprovalNode` modellərini qur.
4. `ApprovalRequest` (Generic FK ilə) modelini yarat.
5. `ApprovalDelegation` modelini qur.
6. `ApprovalLog` modelini yarat.
7. Admin paneldə modellərin qeydiyyatı.
8. `makemigrations` və `migrate` icra et.
9. `ApprovalChain` üçün API serializers yarat.
10. `ApprovalChainViewSet` yarat.
11. `ApprovalRequestSerializer` yarat.
12. `PendingApprovalsView` yarat (Gözləyən tapşırıqlar siyahısı).
13. Təsdiq (Approve) endpoint-ni yaz.
14. Rədd (Reject) endpoint-ni yaz.
15. Yenidən yönləndirmə (Reassign) endpoint-ni yaz.
16. Delegation yaratmaq üçün API yarat.
17. Delegation siyahısı üçün API yarat.
18. `ApprovalExecutionService.approve()` məntiqini yaz (Quorum hesablanması ilə).
19. `DelegationService.get_active_delegate(user)` funksiyasını yaz.
20. `EscalationService.check_escalation_rules()` funksiyasını yaz.
21. Təsdiq zamanı PIN kodu tələb edən əlavə bir layer (Security) yaz.
22. Redis üzərində Delegation cache mexanizmini tətbiq et.
23. `ApprovalRequested` Django signal-ını yarat və konfiqurasiya et.
24. `ApprovalCompleted` signal-ını yarat.
25. Workflow Engine tərəfindən Approval Engine-in çağırılması interfeysini (Facade) yaz.
26. Celery task: `check_expired_approvals()` yarat.
27. Celery task: `deactivate_expired_delegations()` yarat.
28. Notification xidmətini Celery daxilində çağır (Email/Push).
29. N+1 optimizasiyası: Pending list-də hədəf obyektləri gətirmək üçün prefetch yaz.
30. Unit Test: Delegation dövrlərinin yoxlanılması.
31. Unit Test: Quorum (2 of 3) təsdiq məntiqi.
32. Integration Test: Approve və Reject cycle.
33. RBAC/ABAC middleware: `IsAuthorizedToApprove` yoxlaması.
34. Audit: Dəyişikliklərin avtomatik loqlanması mexanizmi.
35. Swagger sənədləşməsinin API detalları ilə yenilənməsi.

## 22. Risklər
- Dairəvi Delegation (A şəxsi B-yə, B şəxsi A-ya icazə verir). Bunun qarşısını alan kod mütləq yazılmalıdır.
- Generic ForeignKey səbəbilə database qeydlərinin çoxaldıqca axtarışın zəifləməsi.

## 23. Prioritet
- **Kritik (P1)**: Workflow Engine-dən dərhal sonra yazılmalıdır, çünki sistemdəki bütün qərarlar buradan keçəcək.
