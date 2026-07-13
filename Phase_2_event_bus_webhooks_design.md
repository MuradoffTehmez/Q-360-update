# Phase 2 - Event Bus & Webhooks Design & Architecture

## 1. Məqsəd
Sistemin daxili modulları arasında (Event Bus) və xarici sistemlərlə (Webhooks) əlaqəni asinxron, decoupling (asılılıqdan azad) formada təşkil etmək. Bir modulda baş verən dəyişikliyi (məs. İstifadəçi yaradıldı) digər modulların (məs. HR, Təhlükəsizlik) dərhal öyrənməsi və öz daxili məntiqlərini işə salması.

## 2. Biznes məqsədi
Sistemin fərqli komponentlərinin bir-birinə birbaşa API call etmədən xəbərləşməsini təmin etməklə inkişaf sürətini (agility) və etibarlılığı artırmaq. Məsələn, "Yeni işçi qəbul edildi" xəbəri olduqda, həm Workflow, həm Mail Server, həm də Active Directory inteqrasiyalarının eyni anda asılı olmadan işə düşməsi. Xarici partnyorlara və ya üçüncü tərəf tətbiqlərə məlumat ötürmək üçün Webhook imkanı.

## 3. Arxitektura
- **Event Bus:** Daxili xəbərləşmə üçün Redis Pub/Sub və ya mövcud Celery broker-i (RabbitMQ/Redis) üzərindən custom event layer (Məs: `django-signals` asinxron formata salınmış halda).
- **Webhooks:** Məlumatın xarici HTTP endpointlərinə göndərilməsi. Göndərilmə prosesi Celery taskları vasitəsilə həyata keçiriləcək. Xarici servislərin API-nə ediləcək Inbound Webhooks da qəbul ediləcək.

## 4. Modul strukturu
```text
q360_project/apps/event_integration/
├── models/
├── services/
├── api/
│   ├── serializers/
│   └── views/
├── receivers/ (Event Bus üçün)
├── senders/ (Webhook out)
└── tests/
```

## 5. Database dəyişiklikləri
### Yeni cədvəllər
- `webhook_endpoint` (Müştərinin qeydiyyatdan keçirdiyi xarici URL-lər)
- `webhook_event` (Hansı hadisələrə abunə olub: `user.created`, `document.signed`)
- `webhook_delivery_log` (Göndərilmə nəticəsi, 200 OK və ya 500 Error, Request/Response payload)

### Əlaqələr və Constraints
- `webhook_event` -> `webhook_endpoint` cədvəlinə bağlıdır.

## 6. API dəyişiklikləri
- **Yeni endpointlər:**
  - `POST /api/v1/webhooks/endpoints/` (Xarici sistemin öz URL-ni qeydiyyatdan keçirməsi)
  - `GET /api/v1/webhooks/logs/`
  - `POST /api/v1/webhooks/inbound/{integration_name}/` (Xaricdən gələn eventləri qəbul edən spesifik endpoint. Məs: MS Teams botundan gələn təsdiq mesajı)

## 7. Servislər (Service Layer)
- `EventPublisherService`: Daxili modullardan gələn eventləri sistemə (bus) yayır.
- `WebhookDispatchService`: Event baş verdikdə abunə olan xarici URL-lərə HTTP sorğusu atır.
- `WebhookSignatureService`: Göndərilən məlumatın Q360-dan gəldiyini təsdiqləmək üçün HMAC (SHA-256) signature yaradır.

## 8. Permission modeli
- Webhook endpoint yaratmaq üçün istifadəçinin xüsusi `Developer` və ya `Integration Admin` rolu olmalıdır. O yalnız öz departamentinə/təşkilatına aid datalara abunə ola bilər.

## 9. Workflow
Workflow Engine təsdiq prosesini bitirdikdə `workflow.completed` eventi atır. Event Bus bunu tutur, abunə olan hər hansı digər modul (məs. HR) öz məntiqini işlədir, həmçinin Webhook modulu bunu müştərinin xarici CRM sisteminə HTTP POST ilə ötürür.

## 10. Event-lər
Sistemin hər modulu öz CRUD və biznes əməliyyatlarına uyğun standart eventlər buraxacaq:
- `user.created`, `user.updated`
- `leave_request.approved`
- `document.signed`

## 11. Security
- Outbound Webhooks: Mütləq HMAC signature header-i əlavə ediləcək. (Məs: `X-Q360-Signature`).
- Server-Side Request Forgery (SSRF) qorunması: İstifadəçinin daxil etdiyi Webhook URL daxili şəbəkə IP-lərinə (`127.0.0.1`, `10.x.x.x`) yönləndirilə bilməz.
- Inbound Webhooks: Yalnız etibarlı IP-lərdən və ya xüsusi API Token vasitəsilə qəbul ediləcək.

## 12. Logging
- Hər göndərilən və qəbul edilən webhook payload-u, HTTP Status kodu, müddəti loglanacaq.

## 13. Performance
- Xarici API-lər yavaş ola bilər. Ona görə webhooklar heç vaxt request/response dövründə (sinxron) atıla bilməz, mütləq Celery queue (məs: `webhook_queue`) üzərindən icra edilməlidir.

## 14. Cache
- Aktiv Webhook URL-ləri və onların abunəlikləri tez-tez DB-dən oxunmamaq üçün in-memory (Redis) saxlanılacaq.

## 15. Background process
- Uğursuz webhook çatdırılmaları (məs: xarici server down olub) üçün **Exponential Backoff** retry məntiqi (məs: 1 dəq, 5 dəq, 30 dəq, 2 saat sonra təkrar yoxlama).

## 16. Test ssenariləri
- HMAC Signature yoxlanılması (Göndərilən signature ilə xarici test serverinin aldığı datadan yaratdığı signature eynidirmi?).
- SSRF bypass cəhdləri (Qadağan olunmuş URL formatları).
- Retry mexanizminin test edilməsi (Mock xarici server 500 qaytardıqda taskın yenidən yaranması).

## 17. Acceptance Criteria
- Sistemdəki istənilən model dəyişikliyi asanlıqla (bir sətir kod və ya mixin ilə) Event Bus-a siqnal ata bilməlidir.
- İstifadəçilər xarici sistemlərini asanlıqla platformaya bağlaya bilməli və sənədləşmədən istifadə edə bilməlidir.

## 18. AI Development Tasks (Mərhələli Tətbiq Planı - ~30 Tapşırıq)

1. `apps/event_integration` modulu yarat.
2. Abstract Pub/Sub interfeysi yaz (daxili xəbərləşmə üçün).
3. Modelleri qur: `WebhookEndpoint`, `WebhookEvent`, `WebhookDeliveryLog`.
4. API Serializer və ViewSet-ləri qur.
5. HMAC Signature generator funksiyasını (`WebhookSignatureService`) yaz və hər endpoint üçün Secret Key generasiyası əlavə et.
6. Xarici URL-lərin validasiyası: SSRF qoruyucu validator yaz (IP/Domain restriction).
7. Celery Task: `send_webhook_payload(endpoint_id, event_type, payload)` yarat.
8. Bu taska daxilində `requests.post()` və timeout məntiqi əlavə et.
9. Task üçün `Exponential Backoff` parametrini təyin et (`autoretry_for=(Exception,), retry_backoff=True, max_retries=5`).
10. `EventPublisherService.publish(event_name, payload)` metodunu yaz.
11. Bu metodun həm daxili `receivers`-lərə, həm də aktiv webhook abunələrinə məlumat göndərməsini təmin et.
12. Sistemin əsas modellərinə (Məs: User) Event Mixin əlavə et (Yaradıldıqda, dəyişdikdə avtomatik publish etsin).
13. Inbound Webhook: Fərqli servislərdən gələn cavabları dinləmək üçün strukturlu View-lar.
14. Unit Test: SSRF validatorunun `192.168.x.x` və ya `localhost` URL-lərini rədd etməsi.
15. Unit Test: HMAC Hash-in düzgün hesablanması.
16. Swagger Documentasiyasına Webhook strukturunu və Header-ləri əlavə et.

## 19. Risklər
- Sistemdə çox sayda eventin (məs. update dövrəsindəki xırda dəyişikliklər) buraxılması Celery queue-nu doldura bilər. Eventlər qruplaşdırılmalı və ya ancaq önəmli field-lər dəyişdikdə atılmalıdır.

## 20. Prioritet
- **Orta (P2)**: Mərkəzi arxitekturanın (Phase 0/1) bərkidilməsindən sonra digər daxili/xarici sistemlərlə inteqrasiya üçün qurulmalıdır.
