# Tam CRUD və Read-Only API Planı

## Məqsəd
Sistemdə mövcud olan 11 fərqli endpoint-in tam CRUD (Create, Read, Update, Delete) və ya yalnız oxunabilən (Read-Only) olması ilə bağlı arxitektur qərarların verilməsi və əsaslandırılması.

## Qərarlar və Əsaslandırmalar

Aşağıdakı 11 resursdan **5-i** təbiəti etibarilə qəsdən **READ-ONLY / GET-ONLY** olaraq saxlanılacaq. Qalan **6 resurs** isə tam `ModelViewSet`-ə keçiriləcək.

### 1. Tam CRUD Olacaq Resurslar (İcra Ediləcək)

#### 1.1. `accounts/roles`
- **Hazırkı:** Ehtimal ki, qismən və ya yalnız read-only.
- **Dəyişiklik:** Tam `ModelViewSet`-ə keçiriləcək. POST, PUT, PATCH, DELETE metodları əlavə olunacaq.
- **Səlahiyyət:** Yalnız `IsAdminUser` (Adminlər) rol yarada, dəyişdirə və silə bilər. Digər autentifikasiyalı istifadəçilər yalnız oxuya bilər.

#### 1.2. `continuous_feedback/public-recognition`
- **Hazırkı:** Qismən (like/comment mümkündür, lakin tam CRUD deyil).
- **Dəyişiklik:** Tam `ModelViewSet`. Təşəkkür mesajını göndərən şəxs onu redaktə edə (PUT/PATCH) və ya silə (DELETE) bilər. `like` və `comment` action-ları toxunulmaz qalacaq.
- **Səlahiyyət:** Yalnız resursun yaradıcısı (və ya admin) dəyişiklik/silmə edə bilər.

#### 1.3. `engagement/badges`
- **Hazırkı:** Nişanların təyinatı (Badge definitions) yalnız oxunabiləndir.
- **Dəyişiklik:** Tam `ModelViewSet`.
- **Səlahiyyət:** Yalnız `IsAdminUser` (HR/Admin) yeni nişan növü yarada, adını/şəklini dəyişdirə və ya ləğv edə bilər.

#### 1.4. `engagement/user-badges`
- **Hazırkı:** İstifadəçilərin qazandığı nişanlar (`ReadOnlyModelViewSet`).
- **Dəyişiklik:** Tam `ModelViewSet`. Avtomatlaşdırılmış sistemlərdən əlavə olaraq rəhbərlik də manual şəkildə istifadəçiyə nişan verə və ya geri ala bilməlidir.
- **Səlahiyyət:** Yalnız Admin və ya menecer nişan verə/silə bilər.

#### 1.5. `performance_reviews` (Notes, Action Items, Competency Evaluations)
- **Hazırkı:** Bu obyektlər sessiya daxilində action olaraq (`add_note`, `evaluate_competency` və s.) istifadə olunur və redaktə/silinmə imkanları məhduddur.
- **Dəyişiklik:** Hər biri üçün müstəqil `ReviewNoteViewSet`, `ReviewActionItemViewSet` və `CompetencyEvaluationViewSet` yaradılacaq. 
- **Səlahiyyət:** Yalnız müvafiq sessiyanın iştirakçıları (menecer, işçi özü) icazə daxilində CRUD edə bilər.

---

### 2. Qəsdən READ-ONLY / GET-ONLY Saxlanılan Resurslar

Aşağıdakı resurslara CRUD (POST/PUT/DELETE) **əlavə edilməyəcək**, çünki bu, sistemin Data Integrity (Məlumat Bütövlüyü) prinsiplərinə ziddir:

#### 2.1. `continuous_feedback/feedback-bank`
- **Səbəb:** Feedback Bank, istifadəçinin aldığı fərdi geridönüşlərin (QuickFeedback) statistik cəmi və analitikasıdır (məsələn, neçə müsbət, neçə mənfi rəy alıb).
- **Əsaslandırma:** Feedback Bank-ın manual yaradılması və ya birbaşa redaktə edilməsi hesabatlarla faktiki rəylər arasındakı riyazi bərabərliyi pozar. O, yalnız tranzaksiyalar üzərindən avtomatik formalaşmalıdır.

#### 2.2. `engagement/engagement-scores`
- **Səbəb:** İstifadəçinin sistemdəki fəallığı (login, təlim tamamlama, rəy bildirmə) əsasında alqoritm tərəfindən hesablanan xaldır.
- **Əsaslandırma:** Bu xalların kənardan PUT/PATCH ilə dəyişdirilməsi gamification (oyunlaşdırma) məntiqini və ədaləti məhv edər. 

#### 2.3. `engagement/leaderboard`
- **Səbəb:** Lider lövhəsi fiziki bir DB cədvəli deyil, `EngagementScore` məlumatlarının xala görə çoxdan-aza sıralanmış dinamik görünüşüdür (View).
- **Əsaslandırma:** Məlumat bazasında "Lider lövhəsi" deyə bir sətir olmadığı üçün yaradılması (POST) və ya silinməsi (DELETE) proqramlaşdırma baxımından mümkünsüzdür. 

#### 2.4. `evaluations/results`
- **Səbəb:** Qiymətləndirmə nəticələri (`EvaluationResult`), kampaniya bitdikdən sonra işçi, rəhbər və həmkarların verdiyi onlarla anket cavabının (EvaluationResponse) riyazi olaraq ortalamasının tapılması yolu ilə çıxarılır.
- **Əsaslandırma:** Birbaşa "Nəticə" obyekti yaratmaq və ya redaktə etmək qiymətləndirmə auditini zədələyər. Nəticə dəyişməlidir? O zaman sistem tərəfindən "Recalculate" action-u çağırılmalıdır.

#### 2.5. `search`
- **Səbəb:** Axtarış modulu dinamik parametrli bir GET sorğusudur (məsələn, `?q=Təhməz`). Sistemdə "SavedSearch" (Yadda saxlanılan axtarış) kimi bir model (DB Table) mövcud deyil.
- **Əsaslandırma:** Model olmadığı üçün bu endpoint yalnız Read-Only qalmalıdır.

#### 2.6. `realtime-stats`
- **Səbəb:** Bu, dashboard üçün real vaxtda onlarla müxtəlif modelin (aktiv istifadəçilər, yarımçıq təlimlər, son audit log-ları) `.count()` sorğuları ilə yığılmış ümumi bir JSON obyektidir.
- **Əsaslandırma:** Aggregated data-ya (ümumiləşdirilmiş hesabat) POST və ya PUT atmaq məntiqsizdir.

## Open Questions / User Review Required

> [!IMPORTANT]
> Zəhmət olmasa, yuxarıdakı **Qəsdən READ-ONLY saxlanılanlar** siyahısını və verilmiş əsaslandırmaları nəzərdən keçirin. "Proceed" düyməsini sıxdıqda mən ilk 5 resursu tam CRUD formata gətirəcək, uyğun icazələri yazacaq, API sənədləşməsini yeniləyəcək və hər biri üçün POST/PUT/DELETE yoxlama testlərini (1 nömrəli maddədəki kimi) işə salacağam.
> Bütün digər 29 xətanın izahatını isə cavab mesajında yazılı olaraq təqdim edirəm.
