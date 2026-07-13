# API INVENTORY

| Modul | Mövcud API (var/yox) | Serializer sayı | ViewSet sayı | Router-ə qeydiyyat (var/yox) | Permission class-lar | Test sayı |
|---|---|---|---|---|---|---|
| accounts | var | 7 | 3 | var | IsAuthenticated, IsSuperAdminOrAdmin, IsOwnerOrAdmin | 50 |
| audit | var | 1 | 1 | var | IsAuthenticated | 2 |
| compensation | var | 4 | 4 | var | IsAuthenticated | 12 |
| competencies | var | 7 | 4 | var | IsAuthenticated | 10 |
| continuous_feedback | var | 11 | 5 | var | IsAuthenticated | 36 |
| dashboard | var | 1 | 1 | var | IsAuthenticated | 4 |
| departments | var | 6 | 3 | var | IsAuthenticated | 0 |
| development_plans | var | 1 | 1 | var | IsAuthenticated | 17 |
| engagement | var | 15 | 8 | var | permissions.IsAuthenticated | 0 |
| evaluations | var | 7 | 6 | var | IsAuthenticated | 27 |
| leave_attendance | var | 5 | 5 | var | IsAuthenticated | 11 |
| notifications | var | 1 | 1 | var | IsAuthenticated | 0 |
| onboarding | var | 1 | 1 | var | IsAuthenticated | 1 |
| performance_reviews | var | 7 | 1 | var | permissions.IsAuthenticated | 3 |
| recruitment | var | 4 | 4 | var | IsAuthenticated | 18 |
| reports | var | 1 | 1 | var | IsAuthenticated | 20 |
| search | var | 1 | 1 | var | IsAuthenticated | 0 |
| security | var | 1 | 1 | var | IsAuthenticated | 1 |
| sentiment_analysis | var | 1 | 1 | var | IsAuthenticated | 0 |
| support | var | 1 | 1 | var | IsAuthenticated | 10 |
| training | var | 9 | 2 | var | IsAuthenticated | 43 |
| wellness | var | 11 | 1 | var | IsAuthenticated | 6 |
| workforce_planning | var | 9 | 4 | var | IsAuthenticated | 7 |

*Qeyd: Bütün modullar artıq DRF Router-ə inteqrasiya olunmuşdur.*

### B. API OLAN LAKİN DRF ROUTER-Ə QOŞULMAYANLAR (0/22)
(Tamamlandı - Bütün modullar Router-ə qoşuldu)

### C. API OLMAYAN MODULLAR (0/22)
(Tamamlandı - Bütün modellərə ViewSet və Serializer əlavə edildi)
