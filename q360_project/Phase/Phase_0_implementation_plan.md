# Phase 0: Platform Refactoring - Implementation Plan

Bu mərhələ Q360 platformasının mövcud monolit və sıx bağlı (tightly coupled) strukturunu Enterprise səviyyəli, mikroservislərə və hadisə əsaslı (Event-Driven) arxitekturaya hazır vəziyyətə gətirmək məqsədi daşıyır. 

Sistemdə hazırda 20-dən çox daxili app (accounts, departments, evaluations və s.) mövcuddur.

## User Review Required
> [!IMPORTANT]
> Bu refaktorinq prosesi sistemin nüvəsində dəyişikliklər edəcək. Yeni baza modelləri və API standartlarının tətbiqi mövcud funksiyaların test edilməsini (Regression testing) tələb edəcəkdir. 
> Aşağıdakı dizayn qərarları ilə razılaşdığınız təqdirdə "Proceed" düyməsini sıxa bilərsiniz.

## Open Questions
> [!WARNING]
> Bütün API cavablarını (Response) vahid formata `{"status": "success", "data": {...}, "message": "..."}` salmaq istəyirsinizmi? Bu mövcud Front-end inteqrasiyalarında kiçik dəyişikliklər tələb edə bilər. (Razısınızsa, xüsusi Renderer/Middleware yazılacaq).

## Proposed Changes

Aşağıdakı addımlar ardıcıl olaraq icra ediləcəkdir:

### 1. Naming Convention & Domain Separation (Service Layer tətbiqi)
Hazırda biznes məntiqləri View-larda və Model metodlarında yerləşir (Məs. `accounts/views.py` daxilində `change_password` məntiqi).
- **[NEW] `apps/core/`**: Bütün ortaq (Core) məntiqlərin cəmlənəcəyi təməl app yaradılacaq.
- **[NEW] `services.py`**: Hər app üçün `services.py` yaradılacaq. View-lar yalnız HTTP Request/Response idarə edəcək, biznes məntiqi service-ə köçürüləcək.

### 2. Enterprise Architecture Review (Base Models)
Bütün cədvəllərin eyni standartda olmasını təmin etmək üçün Core app-də abstrakt modellər yaradılacaq.
- **[NEW] `core/models.py`**: `TimeStampedModel` (created_at, updated_at) və `SoftDeletableModel` (is_deleted, deleted_at) yazılacaq.
- **[MODIFY] Mövcud Modellər**: Mövcud modellər bu baza siniflərdən miras alacaq şəkildə refaktor ediləcək (xüsusən əsas domenlər - User, Department).

### 3. API Standardization
API-lərin enterprise səviyyəsində vahid şəkildə cavab verməsi təmin ediləcək.
- **[NEW] `core/renderers.py`**: DRF üçün Custom JSON Renderer. Uğurlu və xətalı cavabları standartlaşdıracaq.
- **[NEW] `core/exceptions.py`**: Global Exception Handler yazılacaq (500 Errorları loglamaq və istifadəçiyə vahid formatda xəta mesajı qaytarmaq üçün).

### 4. Microservice Readiness & Event Driven Preparation
Gələcək `Event Bus` və asinxron modullar üçün infrastruktur hazırlığı.
- **[NEW] `core/events.py` (və ya `signals.py` yenidən qurulması)**: Modullar arası xəbərləşməni standart Django siqnalları və gələcəkdə asanlıqla Pub/Sub strukturuna (Məs. Kafka/Redis) keçə biləcək interfeyslərlə (Event Dispatcher) qurmaq.

### 5. Dependency Audit
- **[MODIFY] `requirements.txt`**: Təhlükəsizlik boşluğu ola biləcək köhnəlmiş asılılıqların yoxlanması və `pip-audit` tətbiqi ilə təhlükəsizlik hesabatının çıxarılması.

---

## Verification Plan

### Automated Tests
- `pytest` vasitəsilə Core baza modellərinin və Custom Exception/Renderer məntiqinin test edilməsi.
- Refaktor edilmiş `change_password` (və s.) xidmətlərinin Unit Testləri.

### Manual Verification
- Yeni struktura keçdikdən sonra Postman və ya Swagger vasitəsilə API-lərin köhnə qaydada işləməyə davam etməsini (lakin yeni JSON formatı ilə) yoxlamaq.
