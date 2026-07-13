# Phase 4 - Organization Calendar Design & Architecture

## 1. Məqsəd
Təşkilat daxilindəki bütün tədbirlərin, görüşlərin, rəsmi tətillərin, işçilərin məzuniyyət qrafiklərinin vahid və interaktiv təqvim üzərindən idarə edilməsi. Microsoft Exchange (Outlook) və Google Calendar ilə iki tərəfli sinxronizasiya.

## 2. Biznes məqsədi
Şirkət daxilində şəffaflığı artırmaq və görüşlərin planlaşdırılmasında zaman itkisinin (vaxtların toqquşmasının) qarşısını almaq. Əməkdaşlar təqvimdə kimin məzuniyyətdə olduğunu, otaqların (Meeting Rooms) məşğulluq vəziyyətini bir baxışda görə bilsinlər.

## 3. Arxitektura
- **Calendar Data Structure:** iCal (RFC 5545) standartlarına uyğun məlumat modeli.
- **External Sync Engine:** MS Graph API (Outlook üçün) və Google Calendar API ilə periodik (dövri) və Webhook əsaslı sinxronizasiya arxitekturası.

## 4. Modul strukturu
```text
q360_project/apps/organization_calendar/
├── models/
├── services/
│   ├── sync_engines/
│   └── availability/
├── api/
│   ├── serializers/
│   └── views/
└── tests/
```

## 5. Database dəyişiklikləri
### Yeni cədvəllər
- `calendar` (Təqvim adları: HR Təqvimi, Şəxsi Təqvim, IT Təqvimi)
- `calendar_event` (Tədbir: Başlama, Bitmə, Tam gün (All-day), Təkrar (Recurring rule))
- `calendar_attendee` (İştirakçılar və onların cavabı: Accepted, Declined, Tentative)
- `resource` (Otaqlar, proyektorlar və digər rezerv edilə bilən əşyalar)

### Əlaqələr və Constraints
- Recurring (Təkrarlanan) eventlər üçün RRULE stringi saxlanılacaq (məs. `FREQ=WEEKLY;BYDAY=MO,WE,FR`).
- `calendar_event` cədvəlində Xarici API İD-ləri saxlanılacaq (`google_event_id`, `outlook_event_id`).

## 6. API dəyişiklikləri
- **Yeni endpointlər:**
  - `GET /api/v1/calendar/events/` (Date range (start_date, end_date) filtri mütləqdir)
  - `POST /api/v1/calendar/events/`
  - `GET /api/v1/calendar/availability/` (Seçilmiş işçilərin eyni anda boş olduğu vaxtların tapılması)
  - `POST /api/v1/calendar/sync/` (Xarici təqvimlə məcburi sinxronizasiya)

## 7. Servislər (Service Layer)
- `EventService`: Event yaradılması, RRULE parsing.
- `AvailabilityService`: İştirakçıların və otaqların cədvəllərini üst-üstə qoyub (intersection) boş (Free) vaxtları hesablayan servis (Free/Busy məntiqi).
- `ExchangeSyncService` / `GoogleSyncService`: Xarici API-lərlə OAuth2 tokeni istifadə edərək əlaqə.

## 8. Permission modeli
- Təqvimlər Privacy dərəcəsinə malikdir: `Public`, `Private`, `Organization_Wide`.
- Məzuniyyət təqvimləri avtomatik olaraq (HR modulundan) Public (Read-only) olaraq yaradılır.

## 9. Workflow
Bir işçi məzuniyyətə çıxdıqda və təsdiqləndikdə, Workflow Engine HR moduluna xəbər verir. HR modulu `EventService`-ə müraciət edərək şirkət təqviminə "İşçi X Məzuniyyətdədir (Out of Office)" eventi əlavə edir.

## 10. Event-lər
- `EventCreated`
- `EventUpdated`
- `EventCancelled`

## 11. Security
- İştirakçıların şəxsi (Private) görüşlərinin təfərrüatları (Event Title, Description) digər işçilərdən gizlədiləcək, sadəcə təqvimdə "Məşğul (Busy)" kimi görünəcək.

## 12. Logging
- İkili sinxronizasiya zamanı (API xətaları, Token expired) yaşanan texniki çətinliklər loglanacaq.

## 13. Audit
- Otaq (Resource) rezervasiyalarının dəyişdirilməsi / ləğv edilməsi.

## 14. Performance
- Böyük şirkətlərdə hər bir işçinin aylıq minlərlə təqvim datası ola bilər. SQL sorğularında `start_date` və `end_date` üzrə indekslər mütləqdir. Date Range filtirsiz bütün eventlərin gətirilməsi API səviyyəsində qadağan olunmalıdır.

## 15. Cache
- Otaqların ümumi siyahısı və xüsusiyyətləri.

## 16. Background process
- Xarici təqvimlərlə arxa planda Polling (və ya Push dinlənilməsi) Celery vasitəsilə.

## 17. Notification inteqrasiyası
- Yeni görüşə dəvət gəldikdə e-mail (`.ics` faylı qoşularaq) göndərilməsi.
- Tədbirə 15 dəqiqə qalmış Reminder (Push/Email) atılması.

## 18. UI dəyişiklikləri
- FullCalendar.js və ya bənzəri qabaqcıl JS kitabxanası ilə Təqvim Görünüşü (Day/Week/Month/Timeline).
- Otaq məşğulluğunu göstərən Gantt chart bənzəri qrafik.

## 19. Test ssenariləri
- Təkrarlanan (Recurring) eventlərdən müəyyən edilmiş günlərin tam doğru (Dateutil ilə) hesablanması testi.
- Conflict Resolution Test: Eyni anda bir otağı iki nəfər fərqli sorğularla rezerv etməyə çalışdıqda ikincinin rədd edilməsi (Race condition, DB Lock).

## 20. Acceptance Criteria
- Sistemdə iCal (`.ics`) ixrac (Export) və idxal (Import) funksiyası işləməlidir.
- MS Outlook və Google Calendar inteqrasiyaları iki tərəfli (Two-way sync) işləməlidir.

## 21. AI Development Tasks (Mərhələli Tətbiq Planı - ~30 Tapşırıq)

1. `apps/organization_calendar` app-ni yarat.
2. `dateutil` (RRULE üçün) və `icalendar` kitabxanalarını əlavə et.
3. `Calendar`, `Event`, `Attendee`, `Resource` modellərini yarat.
4. `start_date` və `end_date` üçün kompozit index (B-Tree) əlavə et.
5. Serializerlər və FilterBackend-lər (Mütləq Date Range filteri) yaz.
6. API Endpoint: `EventViewSet` yarat.
7. Xüsusi API: Otaqların və işçilərin kəsişmə (Free/Busy) cədvəlini qaytaran `/availability/` endpointi yaz.
8. Recurring event-lərin UI-da tək-tək göstərilməsi üçün RRULE stringindən (məs: hər bazar ertəsi) müvafiq tarixləri çıxaran (Expand) utility funksiya yaz.
9. Dəvətlərə cavab verilməsi üçün `PATCH /events/{id}/attendees/me/` (Accept/Decline) endpointi.
10. Sənəd və məktublara `.ics` faylı generasiya edən funksiya yaz.
11. `MSGraphSyncService` qur: MS Graph API vasitəsilə OAuth2 ilə bağlanıb eventləri oxumaq.
12. `GoogleCalendarSyncService` qur.
13. Xarici ID-ləri xəritələndirən (Mapping) cədvəl və ya JSON sahəsi.
14. Sinxronizasiya konfliktlərini (həm orada, həm burada eyni anda dəyişibsə, son dəyişdirilmə tarixi qalib gəlir məntiqi) yaz.
15. Race condition-ların qarşısını almaq üçün Resource Reservation prosesində DB Transaction Lock (`select_for_update`) istifadə et.
16. Celery Task: Qabaqdan gələn tədbirləri tapıb iştirakçılara xatırlatma (Reminder) e-maili atmaq.
17. Celery Task: Xarici API-lərlə periodik sinxronizasiya.
18. İşə qəbul, məzuniyyət, tətil günlərini avtomatik Public Calendar-a əlavə edəcək Event Receiverlər yaz.
19. Unit Test: RRULE expand testləri.
20. Integration Test: Overlapping (üst-üstə düşən) görüşlərin Availability API-də məşğul (Busy) kimi qayıtması.
21. Swagger Documentasiya yeniləmələri.

## 22. Risklər
- **Timezone Problemləri:** Fərqli ölkələrdən qoşulan işçilərin görüş saatlarının səhv görünməsi. (Həlli: Bütün datalar mütləq UTC formatında DB-də saxlanmalı, yalnız API / UI səviyyəsində lokal timezone-a çevrilməlidir).

## 23. Prioritet
- **Aşağı-Orta (P3)**: Təşkilatın gündəlik həyatı üçün önəmlidir, lakin infrastruktur tam oturduqdan sonra inkişaf etdirilə bilər.
