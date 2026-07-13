# Phase 2 - Background Jobs & Scheduler Design & Architecture

## 1. Məqsəd
Sistemin əsas iş yükünü (API request/response dövrünü) yüngülləşdirmək üçün vaxt aparan və asinxron icra oluna bilən əməliyyatların (məs: e-mail göndərilməsi, hesabat generasiyası, e-imza statusunun yoxlanılması) arxa fona (background) keçirilməsi. Eyni zamanda, periodik işlərin (məs: hər ayın 1-i əmək haqqı hesablanması) planlaşdırılması (Scheduler).

## 2. Biznes məqsədi
İstifadəçi təcrübəsini (UX) yaxşılaşdırmaq. İstənilən düyməyə basıldıqda, əgər proses 1-2 saniyədən çox çəkəcəksə, istifadəçiyə dərhal "Sorğunuz qəbul edildi" mesajını vermək və işi arxada həll etmək. Həmçinin gündəlik, həftəlik və aylıq biznes rutinlərinin insan amili olmadan, avtomatik icrasını təmin etmək.

## 3. Arxitektura
- **Asynchronous Task Queue:** Python/Django ekosistemi üçün standart olan `Celery` + `Redis` (və ya `RabbitMQ`) broker qismində.
- **Scheduler:** Periodik işlər üçün `Celery Beat` istifadəsi, verilənlər bazası üzərindən dinamik idarəetmə üçün `django-celery-beat` kitabxanası.

## 4. Modul strukturu
```text
q360_project/apps/core_infrastructure/
├── tasks/ (Bütün ortaq celery taskları)
├── services/
├── api/
│   ├── serializers/
│   └── views/
└── tests/
```
*Qeyd: Əslində hər app (HR, Workflow) öz daxilində `tasks.py` saxlayacaq. Bu modul yalnız scheduler-in admin idarəetməsi və ortaq taskların monitorinqi üçündür.*

## 5. Database dəyişiklikləri
### Yeni cədvəllər
- `django-celery-beat` tərəfindən avtomatik yaradılan cədvəllər:
  - `crontabschedule`
  - `intervalschedule`
  - `periodictask`
- `task_result` (Django Celery Results tərəfindən avtomatik yaranan - bitmiş taskların statusları və xətaları üçün).

### Əlaqələr və Constraints
- `periodictask` cədvəli interval və ya crontab-a bağlı olur.

## 6. API dəyişiklikləri
- **Yeni endpointlər:**
  - `GET /api/v1/jobs/schedules/` (Mövcud periodik taskların siyahısı)
  - `POST /api/v1/jobs/schedules/` (Yeni schedule yaratmaq)
  - `PUT /api/v1/jobs/schedules/{id}/toggle/` (Taskı dondurmaq/aktivləşdirmək)
  - `GET /api/v1/jobs/status/{task_id}/` (Xüsusi bir asinxron işin bitib-bitməməsini yoxlamaq)

## 7. Servislər (Service Layer)
- `JobSchedulingService`: API üzərindən gələn sorğularla verilənlər bazasında Crontab və ya Interval cədvəllərində qeydiyyat yaratmaq.
- `TaskMonitoringService`: Uğursuz olmuş (Failed) taskların siyahısını çıxarmaq və alert yaratmaq.

## 8. Permission modeli
- Yalnız `System Admin` və `DevOps` rolları periodik taskları əlavə edə, silə və ya dəyişə bilər. Adi istifadəçilər yalnız öz başlatdıqları background taskların statusunu (məs: Excel export) oxuya bilər.

## 9. Workflow
Workflow Engine müəyyən mərhələyə çatdıqda API cavabını gözləmədən Celery taskı işə sala bilər (məs: `send_workflow_email.delay(user_id)`).

## 10. Event-lər
- `TaskFailed`
- `TaskCompleted`

## 11. Security
- Task idarəetmə API-ləri xüsusi icazələr tələb edəcək.

## 12. Logging
- Bütün Celery worker logları mərkəzi loglama sisteminə (ELK/Graylog və ya fayl sisteminə `celery.log`) göndəriləcək.

## 13. Audit
- Kimin hansı vaxtda schedule-i dəyişdirməsi `django-admin` audit loglarında və ya custom audit sistemində saxlanacaq.

## 14. Performance
- Çox sayda taskın eyni anda işə düşməsi DB connection pool-u doldura bilər. Celery worker sayının və `max_connections` parametrlərinin optimal tənzimlənməsi mütləqdir.

## 15. Cache
- Celery Message Broker olaraq onsuz da Redis istifadə edəcək. Task nəticələri (`backend`) qısamüddətli yaddaş üçün Redis-də saxlanıla bilər.

## 16. Background process
- Bu modulun özü məhz background process-lərin nüvəsidir.

## 17. Notification inteqrasiyası
- Task fail olduqda (məsələn ardıcıl 3 dəfə Retry etdikdən sonra), IT Support komandasına Email və ya Slack bildirişi göndərilir.

## 18. UI dəyişiklikləri
- Sistem Administrasiyası bölməsində "Background Jobs & Schedules" səhifəsi.
- İstifadəçi üçün səhifənin yuxarısında "Exporting Excel... 45%" tipli progress bar və ya Notification bell daxilində məlumat.

## 19. Test ssenariləri
- Celery worker-lər üçün `.delay()` funksiyasının çağırılması və nəticənin mock edilməsi testləri.
- Xəta (Exception) atdıqda taskın təyin edilmiş say qədər təkrar cəhd etməsinin (Retry) testi.

## 20. Acceptance Criteria
- Asinxron proseslər API sorğusunun müddətini uzatmamalıdır (API cavabı dərhal qaytarmalıdır).
- Scheduller admin paneldən və ya API üzərindən dinamik dəyişdirildikdə xidmət (celery beat) restart olmadan yeni qaydanı tətbiq etməlidir.

## 21. AI Development Tasks (Mərhələli Tətbiq Planı - ~30 Tapşırıq)

1. Celery, Redis və `django-celery-beat`, `django-celery-results` kitabxanalarını `requirements.txt`-yə əlavə et.
2. `q360_project/celery.py` faylını yarat və standart konfiqurasiyanı yaz.
3. `settings.py`-da Celery broker, result backend və timezone ayarlarını konfiqurasiya et.
4. Tətbiqə `django_celery_beat` və `django_celery_results` app-lərini əlavə et.
5. DB Miqrasiyalarını icra et.
6. Hər mövcud app-də (məs: workflow_engine, access_control) boş `tasks.py` faylı yarat.
7. Base Task Class yarat: Xəta zamanı avtomatik loglama və IT-yə alert atmaq üçün `on_failure` metodunu override et.
8. API: `PeriodicTask` modeli üçün serializer yarat.
9. API: `IntervalSchedule` və `CrontabSchedule` üçün serializer-lər yarat.
10. API: Schedule-lərin idarəsi üçün ViewSet yarat.
11. API: Task statusunu öyrənmək üçün public endpoint (`/status/{task_id}/`) yarat.
12. Retry məntiqi: E-mail və ya xarici şəbəkə asılılığı olan tasklar üçün `@shared_task(bind=True, max_retries=3)` parametrini tətbiq et.
13. Worker monitorinq (Flower) alətinin docker-compose.yml faylına əlavə edilməsi (local dev üçün).
14. Sınaq Taskı: 10 saniyə yatan `dummy_task` yarat və asinxron çağırışı test et.
15. Sınaq Scheduler: Hər saat başı DB-dəki lazımsız qeydləri silən task yaz.
16. Dead-letter queue (çökmüş taskların analizi) mexanizmini və qeydlərini yarat.
17. Unit Test: Celery tasklarını sinxron mühitdə (`CELERY_TASK_ALWAYS_EAGER=True`) test edən konfiqurasiya.
18. Endpointlərin `System Admin` icazəsi ilə qorunmasını (Permission Class) təmin et.
19. Celery Beat schedule cədvəlində dəyişiklik olduqda Beat-in xəbərdar olması üçün siqnal logikasının default işləməsini yoxla.

## 22. Risklər
- **Memory Leak:** Celery worker-lər uzun müddət işlədikdə RAM-ı doldura bilər. Həlli: `CELERY_WORKER_MAX_TASKS_PER_CHILD` parametrinin təyini.
- Redis-in yaddaşının dolması nəticəsində yeni taskların qəbul edilməməsi.

## 23. Prioritet
- **Yüksək (P1)**: Digər funksiyaların sürətli işləməsi və hesabat modullarının qurulması üçün bu infrastruktur ilkin addımlardan biri olmalıdır.
