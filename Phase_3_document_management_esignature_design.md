# Phase 3 - Document Management & Electronic Signature Design & Architecture

## 1. Məqsəd
Təşkilat daxilində yaranan rəsmi sənədlərin (əmrlər, müqavilələr, ərizələr) şablonlar əsasında avtomatik generasiyası, versiyalanması, arxivlənməsi və ən əsası hüquqi qüvvəyə minməsi üçün Elektron İmza (ASAN İmza, SİMA və ya daxili e-imza) ilə təsdiqlənməsi.

## 2. Biznes məqsədi
Kağız dövriyyəsini sıfıra endirmək. İşə qəbul, məzuniyyət, ezamiyyət kimi proseslərdə yaranan sənədlərin fiziki olaraq çap edilib qol çəkilməsi ehtiyacını aradan qaldırmaq. Q360-ı tam rəqəmsal və qanuni sənəd dövriyyəsi (EDO) platformasına çevirmək.

## 3. Arxitektura
- **Document Generation Engine:** HTML/Jinja2 şablonlarından PDF yaradan servis (Məs: `WeasyPrint` və ya `wkhtmltopdf`).
- **Signature Gateway:** Fərqli imza provayderləri (ASAN İmza, SİMA, xarici DocuSign) üçün Vahid Adapter (Facade) pattern-i.
- **Microservice separation:** E-imza əməliyyatları (ASAN imza üçün sertifikat yoxlanışları, SOAP/REST sorğular) asinxron və kəsintiyə həssas olduğu üçün ayrıca bir service/task queue kimi dizayn edilməlidir.

## 4. Modul strukturu
```text
q360_project/apps/document_management/
├── models/
├── services/
│   ├── generators/
│   └── sign_gateways/
├── api/
│   ├── serializers/
│   └── views/
└── tests/
```

## 5. Database dəyişiklikləri
### Yeni cədvəllər
- `document_template` (HTML Şablonlar, Dəyişənlər siyahısı)
- `document` (Generasiya olunmuş sənəd, FileAsset ilə əlaqə, Status: Draft, Pending Signature, Signed, Archived)
- `document_signature` (Sənədə atılmış imzaların xüsusiyyətləri: İmzalanan tərəf, İmzalanma vaxtı, Sertifikat məlumatları, Hash dəyəri)
- `document_version` (Sənəd dəyişdikcə köhnə versiyaların saxlanması)

### Əlaqələr və Constraints
- Sənəd yalnız 1 FileAsset-ə bağlı ola bilər (Hər versiyanın öz faylı var).
- `document` -> `document_signature` (One-to-Many).

## 6. API dəyişiklikləri
- **Yeni endpointlər:**
  - `POST /api/v1/documents/generate/` (Şablona data ötürüb PDF yaratmaq)
  - `POST /api/v1/documents/{id}/sign/initiate/` (ASAN İmza/SİMA prosesini başlatmaq)
  - `GET /api/v1/documents/{id}/sign/status/` (İmza prosesinin anlıq vəziyyətini öyrənmək)
  - `POST /api/v1/documents/sign/callback/` (ASAN İmza/SİMA tərəfindən gələn asinxron cavabı qəbul edən webhook)
  - `GET /api/v1/documents/{id}/versions/`

## 7. Servislər (Service Layer)
- `DocumentGeneratorService`: Verilmiş context-i HTML ilə birləşdirib PDF formatına çevirən servis.
- `SignatureService`: ASAN İmza və ya SİMA API-ləri ilə əlaqə quran, sənədin Hash dəyərini (SHA-256) hesablayıb provayderə göndərən və cavabı gözləyən servis.
- `ValidationService`: Sənədin bütövlüyünü (Integrity) və ona vurulmuş imzanın etibarlılığını yoxlayan servis.

## 8. Permission modeli
- Sənədə imza atmaq üçün istifadəçinin sistemdə qeydiyyatdan keçmiş və doğrulanmış Asan İmza nömrəsi (və ya FİN kodu) olmalıdır.
- Başqasının sənədinə yalnız yetkili şəxslər (Məs. HR) baxa bilər (ABAC).

## 9. Workflow
Workflow Engine təsdiq prosesinin son mərhələsi kimi `Sign Document` step-i yarada bilər. O zaman Workflow Engine Document modulu ilə əlaqəyə girir və istifadəçidən E-İmza tələb edir.

## 10. Event-lər
- `DocumentGenerated`
- `SignatureInitiated`
- `DocumentSigned`
- `SignatureFailed`

## 11. Security
- PDF sənədlərində zərərli kod işləməsinin qarşısını almaq üçün WeasyPrint təhlükəsiz rejimdə (disable JS) çalışdırılacaq.
- ASAN İmza / SİMA ilə əlaqə mütləq TLS 1.2+ və qarşılıqlı (Mutual TLS) sertifikatlarla qorunacaq.
- **Non-repudiation (İmtina edilməzlik):** İmzalanmış sənədin (PDF) üzərinə Q360 tərəfindən Visual xüsusiyyətlər (QR Kod və ya möhür şəkli) və rəqəmsal TimeStamping (Zaman damğası) vurulacaq.

## 12. Logging
- İmzalamanın hər mərhələsi (İstək göndərildi, İstifadəçiyə SMS getdi, İstifadəçi PIN daxil etdi) ardıcıl olaraq loqlanacaq.

## 13. Audit
- Sənəd üzərində olan istənilən dəyişiklik və ya versiya yaranması tamamilə izləniləcək.

## 14. Performance
- Sənəd generasiyası ağır CPU istifadəsi tələb edir. Həmçinin PDF-in Base64 olaraq Asan İmza provayderinə göndərilməsi yaddaş (RAM) tutur. Buna görə bu əməliyyatlar yalnız Celery üzərindən asinxron edilməlidir.

## 15. Cache
- ASAN İmza statusunu yoxlayan (Polling) requestlər üçün müvəqqəti məlumatlar Redis-də tutula bilər.

## 16. Background process
- ASAN İmza əksər hallarda Asinxrondur (Siz sorğu atırsınız, o istifadəçinin telefonuna bildiriş atır, istifadəçi 2 dəqiqə ərzində PIN girir). Bu proses ərzində Celery taskı Polling edəcək və ya Callback (Webhook) gözləyəcək.

## 17. Notification inteqrasiyası
- "X sənədini imzalamağınız gözlənilir" və ya "Sənəd uğurla imzalandı" (Push/SMS).

## 18. UI dəyişiklikləri
- Sənədin önizlənməsi üçün daxili PDF Viewer (PDF.js).
- "İmza at" düyməsi klikləndikdə ekranda Asan İmza kodunun (Verification Code - 4 rəqəmli) göstərilməsi.

## 19. Test ssenariləri
- Saxtalaşdırılmış sənəd testi: İmzalanmış PDF faylına sonradan müdaxilə etdikdə (fayl dəyişdirildikdə) Hash yoxlamasının fail olması (Sənədin ləğvi).
- ASAN İmza timeout testi (İstifadəçi 2 dəqiqə ərzində telefonda PIN daxil etmədikdə).

## 20. Acceptance Criteria
- Hər hansı bir əməliyyat (məs: Məzuniyyət ərizəsi) bitdikdə onun PDF forması avtomatik və fərdi məlumatlarla doldurulmuş şəkildə yaranmalıdır.
- Azərbaycan Respublikası qanunvericiliyinə uyğun olaraq Elektron İmza tətbiq edilməli və fayla (PDF) embed edilməlidir (PAdES formatında).
- Sənəd dəyişdikdə əvvəlki imzalar qüvvədən düşməlidir.

## 21. AI Development Tasks (Mərhələli Tətbiq Planı - ~35 Tapşırıq)

1. `apps/document_management` app-ni yarat.
2. `weasyprint` və `pyHanko` (və ya başqa PDF signing kitabxanası) yüklə.
3. Modelləri qur: `DocumentTemplate`, `Document`, `DocumentSignature`, `DocumentVersion`.
4. Admin paneldə qeydiyyat və miqrasiya.
5. `DocumentTemplate` idarəetməsi (CRUD) üçün API yaz.
6. Jinja2 əsaslı şablona kontekst verib HTML qaytaran test renderi yaz.
7. HTML-dən PDF-ə çevirən `DocumentGeneratorService` funksiyasını yaz.
8. Sənəd generasiyasını asinxron (Celery) edən task yarat.
9. Yaranan PDF-i əvvəl yaratdığımız `file_management` app-inə (S3-ə) yükləyib bağlayan məntiqi yaz.
10. `SignatureGatewayInterface` abstrakt sinfini yarat (Müxtəlif provayderlər üçün baza).
11. `AsanImzaGateway` sinfini yaz (ASAN İmzanın SOAP və ya REST API spesifikasiyasına uyğun - WSDL konfiqurasiyası).
12. (Alternativ) `SimaGateway` sinfini yaz.
13. Sənədin SHA-256 Hash-ni hesablayan və imzalama üçün göndərən endpointi (`/sign/initiate/`) yaz.
14. Cavab olaraq İstifadəçiyə ASAN İmza Yoxlama Kodunu (Verification Code) qaytaran API strukturunu qur.
15. İmza provayderindən cavabı gözləyən Celery Polling Task-ı və ya Webhook endpoint-ni yaz.
16. Provayderdən uğurlu imza gəldikdə onu `DocumentSignature` cədvəlinə yaz.
17. PyHanko (və ya analoji library) istifadə edərək rəqəmsal sertifikatı PDF faylının daxilinə embed (PAdES standartı) et.
18. PDF üzərinə Vizuallaşdırma (Məsələn, son səhifəyə "Rəqəmsal imzalanmışdır, Zaman damğası: X") vuran servis yaz.
19. Sənəddə edilən hər hansı yeniliyin yeni `DocumentVersion` yaratmasını və köhnənin arxivlənməsini təmin et.
20. Hər versiya dəyişikliyində mövcud imzaların "Geçərsiz (Invalidated)" statusuna düşməsini təmin et.
21. Swagger-də Sənəd generasiyası və İmza axınını (Flow) izah et.
22. Unit Test: WeasyPrint ilə HTML-dən PDF yaranması yoxlaması.
23. Unit Test: Şablonda boş qalan dəyişənlərin (Missing context) idarə edilməsi.
24. Unit Test: Hash-lərin (SHA-256) doğruluq yoxlaması.
25. Integration Test: Mocked Asan İmza serveri ilə tam imzalama dövrəsi.
26. Security: WeasyPrint-də şəbəkə girişlərinin (SSRF) bloklanması (`url_fetcher` qadağası).

## 22. Risklər
- **Hüquqi Uyğunluq:** ASAN İmza və rəqəmsal sənədlərin PAdES formatında olması rəsmi dövlət qurumları tərəfindən oxuna bilməli və doğruluğu təsdiq edilə bilməlidir. Xətalı rəqəmsal sertifikat yerləşdirilməsi sənədin etibarsızlığına səbəb olar.

## 23. Prioritet
- **Orta-Yüksək (P1/P2)**: Təşkilatın kağızsız dövriyyəyə (Paperless) keçidi üçün həyati əhəmiyyət daşıyır, amma baza infrastrukturlar (Phase 1, 2) qurulduqdan sonra effektiv işləyəcək.
