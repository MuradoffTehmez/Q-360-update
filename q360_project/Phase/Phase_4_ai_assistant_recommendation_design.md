# Phase 4 - AI Assistant & Recommendation Engine Design & Architecture

## 1. Məqsəd
İstifadəçilərə qərarlar verməkdə, rutin əməliyyatları sürətləndirməkdə (məsələn, "Sabahdan 3 günlük tətil istəyirəm" cümləsini yazdıqda avtomatik ərizə formasını doldurmaq) və təşkilat daxili məlumatları asanlıqla axtarıb tapmaqda kömək edəcək AI (Süni İntellekt) köməkçisi yaratmaq. Həmçinin fərdi istifadəçi davranışlarına əsaslanan tövsiyə mühərriki (məs. təlim tövsiyələri, müvafiq işçi axtarışı) qurmaq.

## 2. Biznes məqsədi
İşçilərin HR, IT və ya Finans departamentlərinə verdiyi standart sualların (Level 1 Support) yükünü avtomatlaşdırmaq. Təşkilatın məhsuldarlığını RAG (Retrieval-Augmented Generation) əsaslı axtarışlarla (Sənəddən suala cavab tapmaq) artırmaq. Data əsaslı (data-driven) idarəetməyə keçid etmək.

## 3. Arxitektura
- **LLM Integration:** OpenAI (və ya Azure OpenAI, self-hosted LLM - Llama 3) ilə API vasitəsilə əlaqə.
- **Vector Database:** Təşkilatın daxili sənədlərini və qaydalarını (Policy Engine) embedding formatında saxlamaq üçün PGVector (PostgreSQL daxili) və ya Qdrant, Pinecone.
- **RAG Pipeline:** İstifadəçi sual verdikdə əvvəlcə Vektor DB-dən ən uyğun məqalələri tapıb context kimi LLM-ə ötürən arxitektura.

## 4. Modul strukturu
```text
q360_project/apps/ai_assistant/
├── models/ (Chat History, Embeddings tracking)
├── services/
│   ├── llm_gateway/
│   ├── vector_search/
│   └── recommendation/
├── api/
│   ├── serializers/
│   └── views/
└── tests/
```

## 5. Database dəyişiklikləri
### Yeni cədvəllər
- `chat_session` (İstifadəçi ilə AI arasındakı söhbətin unik identifikasiyası)
- `chat_message` (Hər bir sual/cavab cütlüyü, Role: User/Assistant)
- `knowledge_document` (RAG üçün vektorlaşdırılmış daxili məlumatların metadata-sı)
- `recommendation_log` (AI-ın istifadəçiyə etdiyi tövsiyələr və istifadəçinin ona verdiyi reaksiya - click, ignore)

### Əlaqələr və Constraints
- Söhbətlər yalnız o söhbəti başlatan istifadəçiyə görünə bilər.

## 6. API dəyişiklikləri
- **Yeni endpointlər:**
  - `POST /api/v1/ai/chat/message/` (Yeni mesaj göndərmək və cavab almaq - Streaming/Server-Sent Events (SSE) ilə)
  - `GET /api/v1/ai/chat/sessions/` (Köhnə söhbətlər)
  - `POST /api/v1/ai/knowledge/sync/` (Sistemdəki yeni qaydaları vektor DB-yə göndərmək)
  - `GET /api/v1/ai/recommendations/` (Ana səhifədə istifadəçiyə özəl tövsiyələr)

## 7. Servislər (Service Layer)
- `LLMService`: OpenAI API ilə əlaqə qurur, Prompt Engineering idarə edir.
- `RAGService`: İstifadəçinin sualını embedding-ə çevirib Vektor DB-də axtarır, ən uyğun 3 nəticəni LLM-ə "System Prompt" kimi verir.
- `ActionParserService`: LLM-in cavabında `{"action": "create_leave_request", "date": "2026-08-01"}` kimi xüsusi JSON formatı gələrsə, onu birbaşa tətbiqin funksiyalarına (Workflow) çevirir.

## 8. Permission modeli
- **Strict ABAC:** AI təşkilatdakı bütün datalara çıxışa malik ola bilər, lakin LLM-ə context kimi yalnız və yalnız sualı verən istifadəçinin **oxuma icazəsi olduğu** (RBAC+ABAC) sənədlər göndərilməlidir.

## 9. Workflow
İstifadəçi Chat-a yazır -> API sualı qəbul edir -> RAGService istifadəçinin icazəsi olan sənədlərdən cavab axtarır -> LLMService Prompt-u hazırlayıb OpenAI-a göndərir -> Streaming vasitəsilə cavab UI-a ötürülür.

## 10. Event-lər
- `ChatSessionStarted`
- `KnowledgeBaseUpdated`

## 11. Security
- **Prompt Injection:** İstifadəçinin zərərli kod və ya prompt daxil edərək AI-ı çaşdırmasının (jailbreak) qarşısını almaq üçün təhlükəsizlik filtrləri.
- **Data Privacy (PII):** Xarici LLM (məs. OpenAI) istifadə edilərsə, şirkətin həssas dataları, FİN kodları API-yə göndərilmədən öncə Anonimləşdirilməlidir (Masking).

## 12. Logging
- Bütün LLM zəngləri (Tokens used, Latency, Cost) analiz və xərc (billing) idarəetməsi üçün `ai_metrics_log` kimi saxlanacaq.

## 13. Audit
- AI-ın istifadəçiyə verdiyi qəti (məsələn, "Sənin 10 gün məzuniyyətin var") cavabların sübutu olaraq Chat History auditi daim saxlanacaq.

## 14. Performance
- OpenAI API cavabları 2-5 saniyə çəkə bilər. İstifadəçi gözləməməsi üçün **Server-Sent Events (SSE)** və ya WebSocket ilə Streaming (hərf-hərf yazılma) tətbiq edilməlidir.

## 15. Background process
- Mövcud məlumat bazasının (Qaydalar, Təlimatlar, User Manullar) vektorlaşdırılması və yeniləndikdə Vektor DB-yə əlavə edilməsi Celery periodik taskı ilə ediləcək.

## 16. UI dəyişiklikləri
- Sistemdə hər yerdən əlçatan olan üzən (Floating) Chatbot widget-ı.
- Dashboard-da "Tövsiyələr" (Suggestions) bloku.

## 17. Test ssenariləri
- Məlumat Məhdudiyyəti (Information Boundary) testi: İşçi AI-dan "CEO-nun maaşı nə qədərdir?" soruşduqda, RAG filterinin bu məlumatı gətirməməsinin yoxlanışı.
- Streaming Connection testi (Qırıntısız məlumat axını).

## 18. Acceptance Criteria
- AI köməkçisi şirkətin daxili qaydaları haqqında (Knowledge Base) verilən suallara <10% halüsinasiya (səhv məlumat uydurma) ilə cavab verməlidir.
- LLM API-yə edilən sorğuların token maliyyətləri hesablanıb qeyd edilməlidir.

## 19. AI Development Tasks (Mərhələli Tətbiq Planı - ~35 Tapşırıq)

1. `apps/ai_assistant` app-ni yarat.
2. `openai` (və ya `langchain`), `pgvector` paketlərini quraşdır.
3. PostgreSQL-də `pgvector` extension-ı aktivləşdir.
4. `ChatSession` və `ChatMessage` modellərini yarat.
5. Vektor datalarını (Embeddings) saxlamaq üçün PGVector Model field-ni yarat (`vector(1536)`).
6. LLM quraşdırmaları (API Keys, Model Name, Temperature) üçün Settings yaz.
7. OpenAI API ilə əlaqə quran baza sinfini yaz (`LLMService`).
8. Mətnləri embedding-ə çevirən (`text-embedding-3-small`) funksiyanı yaz.
9. `RAGService`: Mətni vektorlaşdırıb Vektor cədvəlində Kosinus Oxşarlığı (Cosine Similarity) ilə axtaran DB query-sini yaz.
10. Təşkilati Qaydalar modulundan (Policy Engine) aktiv qaydaları oxuyub Vektor DB-yə (Knowledge Base) dolduran Celery taskı yaz.
11. Data Privacy: Mətndə olan FİN və e-mail-ləri Regex ilə `***` kimi dəyişdirən (Masking) funksiya yaz.
12. LLM üçün "System Prompt" yarat (Məs: "Sən Q360 HR köməkçisisən. Yalnız sənə verilən kontekstə əsaslanaraq cavab ver...").
13. Django `StreamingHttpResponse` (və ya FastAPI inteqrasiyası) istifadə edərək SSE (Server-Sent Events) endpointini yaz.
14. Chat mesajını qəbul edən, asinxron qaydada History-yə yazan API yaz.
15. Function Calling (və ya Tool Use): OpenAI funksiya çağırma xüsusiyyətini əlavə et ki, LLM lazım gəlsə "İstifadəçinin qalan məzuniyyətini hesabla" funksiyasını tətikləyə bilsin.
16. Action Parser: Əgər AI funksiya çağırışı edibsə, onu uyğun Q360 daxili API-sinə yönləndirən router yaz.
17. Recommendation Engine: İstifadəçinin aktivlik tarixinə (Logging modulu) əsaslanaraq "Sizin üçün Faydalı ola bilər" siyahısını hazırlayan sadə Machine Learning (və ya qayda-əsaslı) sinif yarat.
18. AI Metric Modelini yarat: OpenAI cavabındakı `prompt_tokens` və `completion_tokens`-i saxlamaq üçün.
19. Keçmiş Chat Session-ları listələmək üçün ViewSet yaz.
20. Endpointlərdə Rate Limiting əlavə et (Saniyədə n-dən çox sual soruşulmasın, DDoS/Cost abuse qarşısını almaq üçün).
21. Unit Test: Token Masking funksiyasının (Data Privacy) testi.
22. Unit Test: SSE stream generatorun düzgün yield edib etməməsi.
23. Integration Test: Mock OpenAI response verərək RAG promptunun necə formalaşdırıldığını (Context + Question) yoxla.
24. Permission: Vektor axtarışında Row-Level Security (RLS) və ya Django filtrləməsini tətbiq et (İstifadəçi yalnız icazəsi olan şöbənin dokumentlərində axtarış etsin).

## 20. Risklər
- **Hallucination (Uydurma):** LLM olmayan qaydaları varmış kimi təqdim edə bilər. Həlli üçün "Yalnız verilən context daxilində cavab ver, əmin deyilsənsə bilmirəm de" promptu gücləndirilməlidir.
- **Xərclərin artması:** Nəzarətsiz istifadə API fakturalarını şişirdə bilər.

## 21. Prioritet
- **Aşağı (P3)**: Platformanın əsas məlumat strukturları (Phase 1-3) oturduqdan və kifayət qədər "data" formalaşdıqdan sonra əlavə edilməlidir.
