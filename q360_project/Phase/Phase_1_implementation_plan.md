# Phase 1 Execution: Implementation Plan

Bu plan Q360 platformasında "Phase 1: Core Engines" üzrə nəzərdə tutulmuş 5 böyük modulun tam şəkildə (modellər, servislər və API) yazılıb inteqrasiya edilməsini əhatə edir.

Siz `/goal` əmrini verdiyiniz üçün, bu plan təsdiq edildikdən sonra dayanmadan bütün modullar tam hazır olana qədər (uzunmüddətli rejimdə) avtomatik kodlanacaqdır.

## User Review Required
> [!IMPORTANT]
> Bu mərhələ çox böyük miqyaslı kod generasiyası tələb edir. Toplamda 5 fərqli Django Tətbiqi (`apps/*`) yaradılacaq və onlarla cədvəl, API endpoint quraşdırılacaq. Planı gözdən keçirib "Proceed" düyməsini klikləyərək prosesi başladın.

## Open Questions
> [!WARNING]
> Verilənlər bazasının miqrasiyası (`makemigrations` və `migrate`) üçün aktiv (işləyən) PostgreSQL qoşulması (connection) tələb olunur. Hazırkı mühitdə `.venv` və Postgres aktiv olmadığı üçün mən yalnız kod strukturlarını (models.py, views.py, urls.py, services.py) formalaşdıracağam. Əgər sonradan DB-də xəta çıxarsa, müvafiq `.env` quraşdırmalarınızı (məs. DB parolu) özünüz etməlisiniz.

## Proposed Changes

Aşağıdakı komponentlər qruplaşdırılmış şəkildə yazılacaqdır:

### 1. Workflow Engine (`apps/workflow_engine`)
- **[NEW] `models.py`**: `WorkflowTemplate`, `WorkflowStep`, `WorkflowTransition`, `WorkflowCondition`, `WorkflowInstance`, `WorkflowHistory`, `ApprovalAction`.
- **[NEW] `services.py`**: `WorkflowService` (yaratma, başlatma), `TransitionService` (keçid məntiqi).
- **[NEW] `views.py` / `serializers.py`**: CRUD API-lər, `approve`, `reject` action-ları.

### 2. Approval Engine (`apps/approval_engine`)
- **[NEW] `models.py`**: `ApprovalChain`, `ApprovalNode`, `ApprovalRequest`, `ApprovalDelegation`.
- **[NEW] `services.py`**: `ApprovalExecutionService`, `DelegationService` (əvəzetmə).
- **[NEW] `views.py` / `serializers.py`**: Gözləyən təsdiqlərin (pending) listələnməsi və delegation qaydaları.

### 3. RBAC & ABAC (`apps/access_control`)
- **[NEW] `models.py`**: `Role`, `Permission`, `UserRole`, `RolePermission`, `AbacPolicy` (JSON).
- **[NEW] `permissions.py`**: DRF üçün dinamik yoxlama: `IsRbacAuthorized`, `IsAbacAuthorized`.
- **[NEW] `services.py`**: Səlahiyyət qərarlarını verən mərkəzi `AbacEvaluationService`.

### 4. Organization Policy Engine (`apps/policy_engine`)
- **[NEW] `models.py`**: `Policy`, `PolicyRule`, `PolicyVersion`.
- **[NEW] `services.py` / `evaluators.py`**: JSONLogic oxuyaraq input parametrlərindən nəticə çıxaran `PolicyEvaluationService`.
- **[NEW] `views.py` / `serializers.py`**: Siyasətlərin yaradılması və versiyalanması (Activation).

### 5. Feature Flags (`apps/feature_flags`)
- **[NEW] `models.py`**: `FeatureFlag`, `FeatureFlagRule`.
- **[NEW] `utils.py` / `decorators.py`**: Yeni API-ləri qoruyan (söndürüb-yandıran) `@feature_required` dekoratoru.
- **[NEW] `services.py`**: Redis əsaslı və ya DB əsaslı flag vəziyyətini qaytaran `FeatureFlagManager`.

### 6. Layihə səviyyəsində inteqrasiyalar
- Bütün yeni tətbiqlər `config/settings.py`-də `INSTALLED_APPS` siyahısına əlavə ediləcək.
- `config/api_urls.py` (və ya `urls.py`) faylına bu modulların router-ləri qoşulacaq.

---

## Verification Plan

### Automated Tests
*Aktiv bazaya qoşulmaq çətin olduğu üçün, sistem yalnız statik kod səviyyəsində (`manage.py check`) doğrulanacaq.*
- Hər app üçün Python sintaksis yoxlamaları (syntax check) ediləcək.

### Manual Verification
- Plan tamamlandıqda, kodların mövcud arxitekturaya (`TimeStampedModel` və `services.py` qatına) tam oturduğunu yoxlamaq.
- API interfeyslərinin tam və aydın adlandırıldığına (Swagger uyğunluğuna) əmin olmaq.
