# Phase 3 - File & Media Management Design & Architecture

## 1. Məqsəd
Sistemə yüklənən bütün növ faylların (şəkil, video, sənəd, arxiv və s.) mərkəzləşdirilmiş şəkildə saxlanılması, optimallaşdırılması, metadata ilə zənginləşdirilməsi və qlobal əlçatanlığının (S3/CDN vasitəsilə) təmin edilməsi.

## 2. Biznes məqsədi
Mövcud strukturda faylların lokal serverdə (və ya qarışıq qovluqlarda) saxlanılması gələcəkdə disk dolması, ehtiyat nüsxə (backup) çətinlikləri və server köçürülməsi (migration) zamanı problemlər yaradır. Məqsəd faylların idarəetməsini mikroservis arxitekturasına uyğunlaşdırmaq (məs. AWS S3 və ya MinIO istifadə etməklə) və media faylları üçün (şəkil ölçüləndirmə, watermark) mərkəzi emal mühərriki qurmaqdır.

## 3. Arxitektura
- **Storage Backend:** Lokal fayl sistemi yerinə S3 uyğunluqlu (AWS S3, MinIO, rclone) Object Storage arxitekturası.
- **Media Processing Layer:** Şəkillərin kəsilməsi (crop), kiçildilməsi (thumbnail) üçün asinxron və ya on-the-fly (sorğu anında - məs. `thumbor` kimi) emal qatı.
- **CDN (Content Delivery Network):** Tez-tez yüklənən statik və public media fayllarının sürətli çatdırılması üçün.

## 4. Modul strukturu
```text
q360_project/apps/file_management/
├── models/
├── services/
│   ├── storage_backends/
│   └── media_processors/
├── api/
│   ├── serializers/
│   └── views/
└── tests/
```

## 5. Database dəyişiklikləri
### Yeni cədvəllər
- `file_asset` (UUID, Orijinal Adı, Yüklənən Adı, MimeType, Size, S3_Key, Public/Private flag)
- `media_variant` (Əgər şəkildirsə, onun thumbnail, medium, large kimi yaradılmış variantlarının S3 key-ləri)

### Əlaqələr və Constraints
- Digər tətbiqlər (məs: `User.avatar` və ya `LeaveRequest.document`) faylları birbaşa `FileField` kimi deyil, `ForeignKey('file_management.FileAsset')` kimi saxlayacaq.

## 6. API dəyişiklikləri
- **Yeni endpointlər:**
  - `POST /api/v1/files/upload/` (Multipart-form ilə fayl yükləmək)
  - `POST /api/v1/files/upload/presigned/` (Böyük faylları birbaşa S3-ə yükləmək üçün müvəqqəti URL almaq - TÖVSİYƏ EDİLİR)
  - `GET /api/v1/files/{uuid}/` (Fayl haqqında metadata)
  - `GET /api/v1/files/{uuid}/download/` (Məxfi fayllar üçün short-lived (qısamüddətli) download URL qaytarır)

## 7. Servislər (Service Layer)
- `StorageService`: Obyektin S3-ə yazılması, oxunması və silinməsi. Presigned URL-lərin yaradılması.
- `MediaProcessingService`: Pillow və ya xarici kitabxanalar vasitəsilə şəkil ölçülərinin dəyişdirilməsi, metadata (EXIF) təmizlənməsi.
- `FileValidationService`: Yüklənən faylın uzantısının (extension) və əsl MimeType-nin (Magic bytes ilə) yoxlanılması (zərərli skriptlərin qarşısını almaq üçün).

## 8. Permission modeli
- **Public Assets:** Hər kəs link vasitəsilə görə bilər (məs. şirkət loqosu).
- **Private Assets:** Yalnız faylın sahibi və ya sistem tərəfindən icazə verilmiş rollar (məs. işçinin şəxsiyyət vəsiqəsi yalnız HR-a görünməlidir) short-lived URL ilə oxuya bilər.

## 9. Workflow
İstifadəçi sənəd yükləyir -> Sənəd birbaşa S3-ə gedir -> S3 Q360-a "Yükləndi" xəbəri verir (və ya UI arxa fona UUID atır) -> Q360 `FileAsset` yaradır -> Digər modullar həmin UUID-ni istifadə edir.

## 10. Event-lər
- `FileUploaded`
- `FileDeleted`
- `MediaProcessingCompleted`

## 11. Security
- Təhlükəli fayl uzantıları (məs: `.exe`, `.sh`, `.php`) qəti şəkildə rədd edilməlidir.
- Şəkil yüklənərkən daxilində gizlədilmiş zərərli kod (Steganography / XSS payload in SVG) ehtimalına qarşı EXIF datası təmizlənəcək və fayl yenidən render ediləcək.
- S3 Bucket ictimaiyyətə qapalı olacaq (Block all public access), fayllar yalnız Presigned URL-lər vasitəsilə oxunacaq.

## 12. Logging
- Yükləmə xətaları, xüsusən də böyük fayllarda (Timeouts), `storage_log` qeydlərinə düşəcək.

## 13. Audit
- Məxfi sənədlərin (Private Assets) `download/` endpointi üzərindən kim tərəfindən nə vaxt yükləndiyi `audit_log`-a düşəcək.

## 14. Performance
- Fayllar heç vaxt Django (Gunicorn/uWSGI) tərəfindən serve edilməməlidir (Böyük yaddaş itkisi). Yalnız S3 və ya Nginx X-Accel-Redirect istifadə olunmalıdır.

## 15. Background process
- Böyük videoların və ya şəkillərin fərqli ölçülərdə kəsilməsi, sıxılması (compression) Celery Task vasitəsilə asinxron ediləcək. İş bitdikdə WebSocket və ya Notification ilə istifadəçiyə "Media hazırdır" bildirişi gedəcək.
- Orphan files (baza qeydi olmayan və ya heç bir cədvələ bağlanmamış tənha faylların) S3-dən dövri olaraq (məs. həftədə bir) təmizlənməsi (Celery Beat).

## 16. UI dəyişiklikləri
- Mərkəzi "Drag & Drop" fayl yükləmə komponenti (Progress bar ilə).
- Çoxlu fayl yükləmə (Chunked upload - böyük fayllar üçün parçalara bölüb yükləmə).

## 17. Test ssenariləri
- Saxta MimeType testi: `.png` adlandırılmış əslində `.exe` olan faylın sistem tərəfindən bloklanması (python-magic istifadəsi).
- Presigned URL-in müddətinin bitməsi (Expiration) testi.

## 18. Acceptance Criteria
- Fayllar sistemin yaddaşında deyil, konfiqurasiya edilə bilən Object Storage-də saxlanılmalıdır.
- Sistemə yüklənən hər bir fayl mütləq `FileAsset` cədvəlində iz qoymalıdır (Audit üçün).
- Şəkillər yükləndikdə avtomatik olaraq ən azı bir kiçik (thumbnail) versiyası yaranmalıdır.

## 19. AI Development Tasks (Mərhələli Tətbiq Planı - ~35 Tapşırıq)

1. `apps/file_management` app-ni yarat.
2. `boto3` və `python-magic` kitabxanalarını `requirements.txt`-yə əlavə et.
3. `settings.py`-da `DEFAULT_FILE_STORAGE` ayarlarını AWS/MinIO (S3Boto3Storage) üçün konfiqurasiya et.
4. `FileAsset` və `MediaVariant` modellərini yarat.
5. Admin qeydiyyatı və Miqrasiyalar.
6. Validator: MimeType və fayl uzantısını yoxlayan util funksiya yaz.
7. Validator: Maksimum fayl ölçüsünü (Məs: Şəkil üçün 5MB, Video üçün 100MB) yoxlayan məntiq.
8. API Serializer: `FileAssetSerializer`.
9. API Endpoint: `POST /upload/` (Kiçik fayllar üçün standart multipart upload).
10. S3 inteqrasiyası: `StorageService.generate_presigned_post()` metodunu yaz.
11. API Endpoint: `POST /upload/presigned/` (Client birbaşa S3-ə yükləmə edəcək).
12. API Endpoint: S3-ə yükləmə bitdikdən sonra Client-in obyekti təsdiqləməsi (Confirm) üçün `POST /upload/confirm/`.
13. `MediaProcessingService.create_thumbnail(file_uuid)` asinxron funksiyasını yaz (Pillow ilə).
14. Celery Task: `process_media_task(file_uuid)` yarat və `FileUploaded` siqnalı ilə işə sal.
15. API Endpoint: `GET /download/` (Presigned GET URL qaytaracaq, 15 dəqiqəlik).
16. Security: Endpointlərdə Authentication məcburiyyəti (JWT).
17. ABAC Permission Class: `CanAccessFile` (İstifadəçinin bu faylı görməyə haqqı varmı?).
18. Xüsusi Audit Logger: `log_file_download(user, file_uuid)`.
19. Celery Beat Task: `cleanup_orphan_files()` (Son 24 saatda yaranmış amma heç bir modelə bağlanmamış faylları silir).
20. Köhnə `FileField` istifadə edən app-lərin (Məs: User avatar) modelini `ForeignKey(FileAsset)` ilə dəyişmək üçün miqrasiya planı hazırla.
21. Swagger Documentasiyası: Yükləmə prosesinin axınını (Flow) izah et.
22. Unit Test: Magic bytes ilə zərərli fayl qarşısının alınması.
23. Integration Test: Upload, Confirm və Download lifecycle.
24. Integration Test: Thumbnail generasiyasının işləməsi.

## 20. Risklər
- **Geniş miqyaslı Miqrasiya:** Q360-da hazırda fayllar necə saxlanılırsa (məsələn, `/media/` qovluğunda), onların hamısını S3-ə köçürüb DB-də `FileAsset` qeydlərini yaratmaq mürəkkəb bir skript tələb edəcək.

## 21. Prioritet
- **Yüksək (P1)**: Mövcud sistemdə disk dolması və ehtiyat nüsxələşdirmə kimi infrastruktural problemlərin qarşısını almaq üçün mütləqdir.
