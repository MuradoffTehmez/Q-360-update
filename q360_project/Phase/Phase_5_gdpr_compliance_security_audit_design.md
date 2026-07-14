# Phase 5 - Security Hardening, Audit & GDPR Compliance Design

## 1. Məqsəd
Sistemi ən yüksək təhlükəsizlik standartlarına (ISO 27001), Azərbaycan Respublikasının Fərdi Məlumatlar Haqqında qanununa və Avropa Birliyi GDPR tələblərinə uyğunlaşdırmaq. Məlumat sızmalarının qarşısını almaq və hər bir istifadəçi hərəkətinin inkaredilməz izini (Audit Trail) saxlamaq.

## 2. Biznes məqsədi
Q360 platformasının dövlət və ya böyük maliyyə/korporativ müştərilərə (Enterprise) satıla bilməsi üçün tələb olunan hüquqi və texniki sertifikasiyalardan (Penetration Testing, Compliance Audit) keçməsini təmin etmək. Şirkəti yüksək cərimələrdən qorumaq.

## 3. Arxitektura
- **Audit Logging:** Əməliyyat (Transactional) cədvəllərlə Audit cədvəlləri tamamilə ayrılacaq. Audit dataları bəzən RDBMS-dən (PostgreSQL) fərqli olaraq Append-Only Data Store (məs: ElasticSearch və ya TimescaleDB) kimi yerlərdə saxlanıla bilər.
- **Data Encryption (Şifrələmə):** DB səviyyəsində Həssas məlumatların (FİN kod, Əmək haqqı, Parollar) At Rest (sükunət halında) şifrələnməsi.

## 4. Modul strukturu
```text
q360_project/apps/compliance_security/
├── models/ (AuditLogs, DataSubjectRequests)
├── middlewares/ (Security headers, Rate limiting)
├── services/
│   ├── encryption_service/
│   └── gdpr_service/
├── api/
└── tests/
```

## 5. Database dəyişiklikləri
### Yeni cədvəllər
- `audit_log` (Hər bir HTTP request və DB dəyişikliyi: IP, User Agent, Endpoint, Old Payload, New Payload)
- `consent_record` (İstifadəçinin fərdi məlumatlarının işlənməsinə verdiyi razılıqların tarixi)
- `data_subject_request` (GDPR tələbi: Məlumatımı sil (Right to be forgotten), Məlumatımı ver (Data Portability) sorğuları)

### Əlaqələr və Constraints
- Audit Log cədvəlində Dəyişdirilməzlik (Immutability) təmin edilməlidir. Heç bir halda `UPDATE` və ya `DELETE` işləməməlidir (Database Trigger və ya user permissions ilə əngəllənməlidir).

## 6. API dəyişiklikləri
- **Yeni endpointlər:**
  - `GET /api/v1/audit/logs/` (SuperAdmin üçün)
  - `POST /api/v1/compliance/dsr/` (İstifadəçinin öz məlumatlarını silmək və ya endirmək üçün rəsmi müraciəti)
  - `GET /api/v1/compliance/export-my-data/` (İstifadəçiyə aid hər şeyi ZIP formatında verən API)

## 7. Servislər (Service Layer)
- `AuditTrailService`: Model dəyişikliklərini (Django Signals `post_save`, `post_delete` ilə) avtomatik tutub `audit_log`-a yazan servis.
- `EncryptionService`: Model field-lərini AES-GCM və s. standartlarla şifrələyib açan servis.
- `GdprService`: "Right to be forgotten" qanunu çərçivəsində, silinməsi tələb olunan məlumatları tapıb silən (və ya maliyyə sənədlərində adları anonimləşdirən) məntiq.

## 8. Permission modeli
- **Heç kim** (hətta System Admin belə) Audit Log-ları silə bilməz. (Bu, DB səviyyəsində DBA (Database Administrator) icazələri ilə məhdudlaşdırılır).
- Həssas məlumatlar (əmək haqqı kimi) DB-də şifrəlidir, API-dən bunu görmək üçün yalnız xüsusi ABAC Policy-si olanlar icazə ala bilər.

## 9. Workflow
Data silinmə sorğusu gəlir -> Data Protection Officer (DPO) təsdiqləyir (Workflow Engine vasitəsilə) -> GdprService işə düşür və istifadəçini anonimləşdirir.

## 10. Event-lər
- `SecurityBreachAttempted` (Məs. eyni IP-dən 50 yanlış login cəhdi)
- `DataExportRequested`
- `UserDataAnonymized`

## 11. Security Hardening Tədbirləri
- **Rate Limiting / Throttling:** Bütün API-lərdə, xüsusən `login/`, `forgot-password/` endpointlərində.
- **Security Headers:** `Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options` mütləq olacaq.
- **Session Management:** Hərəkətsizlikdən sonra (Inactivity timeout) məcburi log-out. İkili doğrulamadan (2FA) istifadə məcburiyyəti.
- **SQL Injection & XSS:** Django ORM və Template sistemi bizi əsasən qoruyur, amma API girişlərində Pydantic/DRF validation çox sərt olacaq. Payload daxilində JS icrası təmizlənəcək (Sanitization).

## 12. Logging & Audit
- Bu modulun özü məhz bu iş üçün nəzərdə tutulub. Milyonlarla sətir log yaranacağı üçün köhnə logların S3-ə və ya soyuq yaddaşa (Cold Storage) arxivlənməsi (Archiving) strategiyası qurulacaq.

## 13. Performance
- Hər DB update əməliyyatının Audit log-a yazılması əlavə I/O yüküdür. Bunun üçün Django daxili `post_save` siqnalları əvəzinə PostgreSQL `Trigger`-ləri, ElasticSearch inteqrasiyası və ya Kafka asinxron message queue istifadə edilə bilər (Enterprise miqyası üçün).

## 14. UI dəyişiklikləri
- Qeydiyyat/Login zamanı Cookie razılığı (Consent banner).
- İstifadəçi profilində "Privacy & Security" bölməsi (Sessiyaları idarə etmək, 2FA aktivləşdirmək, Datanı export etmək).

## 15. Test ssenariləri
- Penetration Testing ssenariləri: CSRF token olmayan saxta POST cəhdləri, SQL injection payloadları (`' OR 1=1 --`).
- Anonimləşdirmə testi: İstəfadəçi silindikdən sonra onun iştirak etdiyi Məzuniyyət təsdiq zəncirində adının sistemin işini pozmayacaq formada "Deleted User" kimi dəyişməsi.

## 16. Acceptance Criteria
- Hər hansı bir modeldə edilən dəyişiklik avtomatik, kod əlavə etmədən Audit Log-da əvvəlki və sonrakı vəziyyəti (JSON diff) ilə görünməlidir.
- Fərdi məlumatları ehtiva edən cədvəl sütunları DB-də şifrələnmiş formada oturmalıdır (Hardware/Software Key Management istifadə edərək).
- API-lər ən son OWASP Top 10 standartlarına uyğun təhlükəsizlik testlərindən keçməlidir.

## 17. AI Development Tasks (Mərhələli Tətbiq Planı - ~35 Tapşırıq)

1. `apps/compliance_security` app-ni yarat.
2. `django-axes` (Brute-force qorunması), `django-auditlog` (və ya custom audit), `cryptography` kitabxanalarını əlavə et.
3. Django settings-də bütün Security Middleware-ləri (XFrameOptions, SecurityMiddleware, s.) aktivləşdir və tənzimlə.
4. `AuditLog` cədvəlini (Action, Actor, ResourceType, ResourceID, Pre_state_JSON, Post_state_JSON, IP) yarat.
5. Django `post_save`, `post_delete` siqnalları vasitəsilə mühüm modellərin (User, Salary, Leaves) dəyişikliklərini dinləyib `AuditLog`-a yazan mexanizm qur.
6. HTTP Request zamanı istifadəçi (User) və IP məlumatlarını siqnallara çatdırmaq üçün `ThreadLocal` middleware (və ya `django-crum`) tətbiq et.
7. AES Şifrələməsi üçün Key Management məntiqini `settings.py`-də (və ya xarici .env) qur.
8. Custom Django Model Field yarat: `EncryptedCharField`. Databazaya yazanda şifrələsin, oxuyanda açsın.
9. Bu Field-i həssas məlumatlara (FİN kod, pasport nömrəsi) tətbiq edib DB miqrasiya et.
10. `DataSubjectRequest` modelini yarat.
11. İstifadəçinin bütün məlumatlarını (Məzuniyyətlər, İmzalar, Mesajlar) toplayıb bir JSON/ZIP faylına yığan (`Data Export`) asinxron Celery Task yaz.
12. "Right to be forgotten" tətbiqi: İstifadəçi obyekti silindikdə onun bağlı olduğu digər cədvəllərdəki datanı kaskad silmək əvəzinə anonimləşdirən (adını Null və ya Hash edən) təmizlik funksiyasını yaz.
13. API səviyyəsində Rate Limiting (DRF `AnonRateThrottle`, `UserRateThrottle`) konfiqurasiyası et.
14. İki Mərhələli Doğrulama (2FA - TOTP/Authenticator App) üçün lazımi endpoinləri və modelləri yaz (`django-otp` və ya custom).
15. Sessiya təhlükəsizliyi: Bir istifadəçinin başqa brauzerdəki (və ya aktiv) sessiyalarını siyahılamaq və məcburi bağlamaq (Revoke token) üçün API yaz.
16. DB Səviyyəsində qoruma: `AuditLog` cədvəli üçün PostgreSQL səviyyəsində `CREATE RULE` yazaraq `UPDATE/DELETE` əməliyyatlarını blokla.
17. Dövri task: 1 ildən köhnə Audit Logların S3-ə JSON Lines (.jsonl.gz) formatında arxivlənməsi və bazadan təmizlənməsi.
18. Xüsusi Security Dashboard ViewSet yaz: SuperAdmin-ə qeyri-adi fəaliyyətləri (Anomaly detection) göstərən.
19. Unit Test: EncryptedCharField-in bazaya plain text (açıq mətn) yazmadığının (SQL səviyyəsində yoxlanması) testi.
20. Integration Test: 2FA aktiv olduqda standart `/token/` API-nin cavab qaytarmaması və ya əlavə OTP tələb etməsi.
21. Swagger Documentasiyasını Security Authorization Headers ilə yenilə.

## 18. Risklər
- **Açar itkisi:** Şifrələmə üçün istifadə olunan Master Key (AES Key) itirilərsə və ya kompromat olarsa, bütün həssas datalar oxunmaz hala gələcək. Key rotation (açarların mütəmadi dəyişdirilməsi) və backup mexanizmləri kritikdir.
- Sistem performansı çox güclü audit səbəbilə aşağı düşə bilər.

## 19. Prioritet
- **Kritik, lakin sona yaxın (P1/P2)**: Arxitekturanın təməli yazılarkən nəzərə alınmalıdır (xüsusən Audit və Şifrələmə), lakin əsas biznes funksionallıqları (HR, Workflow) bitdikdən sonra tam Hardening aparılmalıdır.
