Q360 platformasının BÜTÜN səhifələrini (təkcə Landing/Haqqımızda/FAQ 
deyil — dashboard, evaluations, reports, departments, competency framework, 
9-box grid, succession planning, bütün autentifikasiyalı və açıq səhifələr 
daxil olmaqla TAM SİYAHI) əhatə edən hərtərəfli frontend audit, mobil 
uyğunluq (responsive) düzəlişi və performans optimallaşdırması apar. 
Bütün mərhələləri ARDICIL, DAYANMADAN, TƏSDİQ GÖZLƏMƏDƏN icra et — bu, 
avtonom bir tapşırıqdır. Yalnız aşağıdakı hallarda dayan: (a) mövcud 
funksionallığı poza biləcək qərar qarşısında qalsan, (b) tələb olunan 
credential/məlumat yoxdursa, (c) gözlənilməz struktur mürəkkəbliyi 
(standart yanaşma işləməyəndə) aşkar olunsa. Əks halda ən məntiqli 
qərarı özün ver, qeyd et və davam et.

ÜMUMI QAYDALAR:
- Hər addımdan sonra öz-özünü yoxla: docker compose exec web python 
  manage.py check və docker compose logs web --tail=30 ilə xəta 
  olmadığını təsdiqlə, xəta varsa dərhal düzəlt, sonra davam et
- Hər dəyişiklikdən sonra müvafiq səhifənin həm masaüstü, həm mobil 
  (375px, 768px) ölçüdə vizual olaraq düzgün qaldığını yoxla (ekran 
  görüntüsü çək, YEKUN HESABATA daxil et, amma söhbətin ortasında 
  ayrıca göstərmə)
- Mövcud dizayn dilini (Tailwind rəngləri, komponent stili) qoruyaraq 
  düzəliş et — struktur dəyişikliyi lazımdırsa, mövcud pattern-lərə uyğun et
- Bütün tapılan problemləri, tətbiq olunan düzəlişləri, qərar 
  gerekçelerini bir jurnal kimi qeyd et — bunlar yekun hesabatda 
  istifadə olunacaq
- Autentifikasiya tələb edən səhifələri test etmək üçün mövcud test 
  istifadəçisi credentials-dan istifadə et; yoxdursa, YALNIZ bu halda 
  dayanıb soruş

═══════════════════════════════════
MƏRHƏLƏ 0 — SƏHİFƏ İNVENTARI
═══════════════════════════════════
1. Bütün urls.py fayllarını gəzərək platformadakı BÜTÜN unikal 
   səhifə/route siyahısını çıxar
2. Açıq/autentifikasiyalı, sadə/orta/mürəkkəb olaraq təsnif et
3. Bu siyahını daxili işçi sənəd kimi saxla, sonrakı mərhələlərdə istifadə et

═══════════════════════════════════
MƏRHƏLƏ 1 — MOBİL RESPONSIVE AUDİT VƏ DÜZƏLİŞ (HƏR SƏHİFƏ)
═══════════════════════════════════
Hər səhifəni bu ekran ölçülərində (375px, 390px, 768px, 1024px, 1440px) 
sınaqdan keçir və TAPILAN PROBLEMLƏRİ DƏRHAL DÜZƏLT (ayrıca təsdiq 
mərhələsi gözləmə):

1. Horizontal scroll / viewport-dan kənara çıxma
2. Cədvəllərin mobil ekranda kəsilməsi (overflow-x-auto və ya kart 
   görünüşünə çevrilmə)
3. Toxunma hədəfi ölçüləri (minimum 44x44px)
4. Mətn ölçüsü/sıxlığı (font-size minimum 12px, oxunaqlılıq)
5. Forma sahələrinin mobil klaviatura ilə problemsiz işləməsi 
   (font-size minimum 16px, iOS avtomatik zoom problemi olmasın)
6. Modal/dropdown/popup-ların mobil ekranda düzgün mövqelənməsi
7. Fixed/sticky elementlərin mobil scroll ilə konflikt yaratmaması
8. Qrafik/chart komponentlərinin (Competency Framework, 9-Box Grid) 
   kiçik ekranda oxunaqlı qalması
9. Sidebar/naviqasiyanın mobil collapse/hamburger məntiqi
10. Flexbox/Grid düzülüşlərinin kiçik ekranda sinməməsi

Hər düzəlişdən sonra: (a) həmin səhifəni bütün 5 ölçüdə yenidən yoxla, 
(b) paylaşılan komponentə (navbar, footer, form widget) toxunulubsa, 
təsirlənən BÜTÜN digər səhifələri də yoxla ki, requssiya yaranmasın.

═══════════════════════════════════
MƏRHƏLƏ 2 — ÜMUMİ FRONTEND PROBLEM AUDİTİ VƏ DÜZƏLİŞ
═══════════════════════════════════
Hər səhifədə aşağıdakıları tap və düzəlt:

1. KONSOL XƏTALARI: DevTools Console-da JS error/warning-ları tap, 
   səbəbini araşdır, düzəlt
2. ŞƏBƏKƏ SORĞULARI: 404/500 statuslu sorğuları (sınıq şəkil/font/API 
   linki), lazımsız təkrarlanan sorğuları tap və düzəlt
3. N+1 QUERY PROBLEMİ: Django Debug Toolbar/django-silk ilə hər 
   səhifənin DB sorğu sayını ölç, 50-dən çox sorğu aparan səhifələri 
   select_related/prefetch_related ilə optimallaşdır
4. TƏKRARLANAN KOD: Bir neçə template-də təkrarlanan CSS/JS məntiqini 
   paylaşılan component/partial-a çıxar
5. FORM VALİDASİYASI: Client-side validasiyanın mövcudluğunu, server 
   xətalarının aydın göstərilməsini təmin et
6. LOADING STATE-LƏR: AJAX/fetch sorğularına spinner/skeleton əlavə et
7. XƏTA VƏZİYYƏTLƏRİ: Boş məlumat və şəbəkə xətası hallarında 
   istifadəçi mesajlarının mövcudluğunu təmin et

═══════════════════════════════════
MƏRHƏLƏ 3 — SƏHİFƏ YÜKLƏNMƏ SÜRƏTİ OPTİMALLAŞDIRMASI
═══════════════════════════════════
QEYD: Tam səhifə yüklənməsi üçün 80-100ms fiziki olaraq mümkün deyil 
(minimum HTTP round-trip bundan uzundur). Real, ölçülə bilən hədəflər:
- SERVER RESPONSE TIME (TTFB): 80-150ms-ə qədər — bu, bizim nəzarət 
  edə biləcəyimiz əsas metrikadır, buna maksimum diqqət yetir
- Tam səhifənin Time to Interactive: 1.5-2.5 saniyəyə qədər

Hər səhifə üçün:
1. Django Debug Toolbar/django-silk ilə server-side emal vaxtını ölç
2. 150ms-dən çox çəkən view-ları prioritetləşdir və optimallaşdır:
   - N+1 query-ləri düzəlt
   - Təkrarlanan/lazımsız sorğuları aradan qaldır
   - Ağır hesablamaları Redis/Django cache ilə keşlə (məlumatın 
     yenilənmə tezliyinə uyğun TTL seç)
   - Böyük queryset-lərə pagination əlavə et
3. Hər səhifə üçün yalnız lazım olan CSS/JS-in yükləndiyini təsdiqlə 
   (lazımsız kitabxanaları o səhifədən çıxar)
4. Əvvəl/sonra server response time, sorğu sayı, statik fayl ölçüsünü 
   jurnalına qeyd et (yekun hesabatda istifadə üçün)

═══════════════════════════════════
MƏRHƏLƏ 4 — "TAM SƏHİFƏ YENİDƏN YÜKLƏNMƏSİ" PROBLEMİNİN HƏLLİ
═══════════════════════════════════
İstifadəçinin kiçik dəyişiklikləri (filter seçimi, form doldurma, sətir 
redaktəsi, status dəyişikliyi) BÜTÜN səhifənin yenidən yüklənməsinə 
(full page reload) səbəb olan bütün yerləri tap və AJAX/fetch əsaslı 
qismən yeniləməyə (partial update) keçir:

1. Bütün <form> taqlarını tap, tam submit (reload) edənləri müəyyən et
2. Prioritetləşdir və tək-tək düzəlt:
   - Filter/axtarış formaları
   - Cədvəl daxilində sətir statusu dəyişikliyi (təsdiqlə/sil düymələri)
   - Pagination (yalnız cədvəl hissəsi yenilənsin)
   - Modal-daxili formalar
3. Django view-larını JSON cavab da qaytara bilən şəklə uyğunlaşdır 
   (və ya ayrıca API endpoint), frontend-də fetch() ilə sorğu göndər, 
   yalnız aidiyyəti DOM hissəsini yenilə. Layihədə Alpine.js istifadə 
   olunduğu üçün Alpine-in reaktivlik imkanlarından, tələb olunarsa 
   HTMX-dən istifadə et (hansının mövcud stack-ə uyğun olduğuna öz 
   qərarını ver və gerekçeni jurnalına yaz)
4. Brauzer tarixçəsinin (back/forward, URL yenilənməsi) düzgün 
   işlədiyini təsdiqlə
5. Hər AJAX sorğusuna loading state (spinner) əlavə et

Bu mərhələni ən diqqətli şəkildə, hər forma/interaksiyanı ayrı-ayrı 
tətbiq və test edərək icra et (funksionallıq pozulmasın deyə).

═══════════════════════════════════
MƏRHƏLƏ 5 — YEKUN VALİDASİYA VƏ REQRESSİYA TESTİ
═══════════════════════════════════
1. Mərhələ 0-da siyahılanan BÜTÜN səhifələri yenidən, bütün 5 ekran 
   ölçüsündə vizual test et
2. Hər səhifədə əsas funksionallığın (forma göndərmə, filter, 
   naviqasiya, AJAX interaksiyalar) hələ işlədiyini təsdiqlə — 
   REQRESSİYA VARSA DƏRHAL DÜZƏLT
3. Bütün açıq səhifələr üçün Lighthouse auditini təkrar icra et
4. Server response time-ların yekun cədvəlini hazırla

═══════════════════════════════════
YEKUN HESABAT (YALNIZ BU MƏRHƏLƏDƏ TƏQDİM ET)
═══════════════════════════════════
Bütün işlər bitdikdən sonra, TƏK BİR detallı yekun hesabat hazırla 
(Markdown fayl kimi saxla və məzmununu də göstər), aşağıdakı bölmələrlə:

1. **İcra Xülasəsi** — neçə səhifə audit edildi, neçə problem tapıldı, 
   neçəsi həll olundu
2. **Səhifə İnventarı** — Mərhələ 0-dakı tam siyahı
3. **Mobil Responsive Düzəlişlər** — hər səhifə üzrə: tapılan problemlər, 
   tətbiq olunan həll, əvvəl/sonra ekran görüntüsü (fayl yolu referansı)
4. **Ümumi Frontend Problemləri** — konsol xətaları, N+1 query-lər, 
   sınıq linklər və s. — nə tapıldı, necə düzəldildi
5. **Performans Nəticələri** — hər səhifə üzrə əvvəl/sonra: server 
   response time, DB sorğu sayı, Lighthouse xalları (Performance/SEO/
   Accessibility/Best Practices), LCP/FCP/TBT/CLS
6. **AJAX/Partial Update Dəyişiklikləri** — hansı formalar/interaksiyalar 
   tam reload-dan AJAX-a keçirildi, hansı texnologiya (Alpine/HTMX) 
   seçildi və niyə
7. **Dəyişdirilən Bütün Faylların Tam Siyahısı**
8. **Həll Olunmayan/Gələcək İş kimi Qeyd Olunan Məsələlər** — texniki 
   məhdudiyyətlər səbəbindən bu mərhələdə görülməyən işlər, gerekçesi ilə
9. **Requssiya Test Nəticələri** — hər səhifədə funksionallığın 
   qorunduğunun təsdiqi

Bu hesabatdan başqa, iş prosesi boyunca əlavə açıqlama, aralıq status 
yeniləməsi və ya təsdiq sorğusu GÖNDƏRMƏ — sadəcə işlə və sonda 
hesabatı təqdim et.


## Frontend Audit & Optimallaşdırma Tapşırığı

Q360-un BÜTÜN səhifələrini (dashboard, evaluations, reports, departments,
competency framework, 9-box grid, succession planning, açıq səhifələr
daxil) əhatə edən frontend audit apar. Avtonom işlə, dayanmadan, təsdiq
gözləmədən — yalnız funksionallığı poza biləcək qərar, çatışmayan
credential, ya da gözlənilməz struktur mürəkkəbliyi olanda dayan.

Hər addımdan sonra: `docker compose exec web python manage.py check` və
`docker compose logs web --tail=30` ilə xəta yoxla, tapsan dərhal düzəlt.
Mövcud Tailwind dizayn dilini qoru. Bütün tapıntı/düzəliş/qərarları
jurnala yaz (yekun hesabat üçün).

**Mərhələ 0 — İnventar:** Bütün urls.py-ları gəzib tam səhifə siyahısı
çıxar (açıq/auth, sadə/mürəkkəb təsnifatı ilə).

**Mərhələ 1 — Mobil Responsive:** Hər səhifəni 375/390/768/1024/1440px-də
yoxla və DƏRHAL düzəlt: horizontal scroll, cədvəl overflow, tap-target
44x44px, font-size (input min 16px – iOS zoom bug), modal mövqeyi,
fixed/sticky konflikt, chart-ların mobil oxunaqlılığı, sidebar collapse,
grid/flex sınması. Paylaşılan komponentə toxunulanda təsirlənən BÜTÜN
səhifələri yenidən yoxla.

**Mərhələ 2 — Ümumi Frontend Problemləri:** Konsol xətaları, 404/500
sorğular, N+1 query (django-silk/debug-toolbar ilə, 50+ sorğu olan
səhifələri select_related/prefetch_related ilə düzəlt), təkrarlanan kod,
forma validasiyası, loading state, boş/xəta vəziyyəti mesajları.

**Mərhələ 3 — Sürət:** Hədəf: server response (TTFB) 80-150ms, Time to
Interactive 1.5-2.5s (tam səhifə 80-100ms fiziki mümkün deyil, TTFB-yə
fokuslan). 150ms+ view-ları optimallaşdır (query, cache, pagination).
Hər səhifədə yalnız lazımi CSS/JS yüklənsin.

**Mərhələ 4 — Partial Update:** Tam səhifə reload edən formaları (filter,
sətir statusu, pagination, modal-daxili formalar) tap, Django view-ları
JSON da qaytara bilən et, Alpine.js (və ya uyğunsa HTMX) ilə fetch-əsaslı
qismən yeniləməyə keçir. Back/forward tarixçəsini, loading spinner-i təmin et.

**Mərhələ 5 — Requssiya Testi:** Bütün səhifələri yenidən vizual+funksional
yoxla, Lighthouse-u təkrar işlət.

**Yekun Hesabat (yalnız sonda, bir dəfə):** Markdown fayl kimi saxla —
icra xülasəsi, səhifə inventarı, mobil düzəlişlər (əvvəl/sonra skrinşot
referansı), ümumi problemlər, performans nəticələri (TTFB, query sayı,
Lighthouse xalları/LCP/FCP/TBT/CLS əvvəl-sonra), AJAX dəyişiklikləri,
dəyişdirilən fayllar siyahısı, həll olunmamış məsələlər, requssiya
nəticələri. Proses boyu ARA HESABAT/TƏSDİQ SORĞUSU GÖNDƏRMƏ.