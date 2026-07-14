---
name: db-optimizasiya
description: >
  Q360 layihəsində Django ORM istifadə edərkən database optimizasiyası, N+1 problemi həlledilməsi,
  düzgün indeksləmə, kompleks sorğuların (aggregation/annotation) qurulması və queryset
  performansının artırılması qaydaları. Tetikleyicilər: "optimizasiya et", "n+1 problemi",
  "database sürətləndir", "query optimizasiya", "select_related", "prefetch_related",
  "slow query", "orm optimizasiya".
---

# Database Optimizasiyası — Q360

Q360 platforması yüksək trafik və böyük məlumat həcmi (minlərlə qiymətləndirmə nəticələri) ilə işlədiyinə görə, verilənlər bazası (PostgreSQL) sorğularının performansı kritikdir.

## 1. N+1 Sorğu Probleminin Qarşısının Alınması

N+1 problemi, siyahıdaki hər bir obyekt üçün əlaqəli məlumatı əldə etmək üçün əlavə bir verilənlər bazası sorğusunun icra edilməsidir.

### ForeignKey və OneToOneField üçün (`select_related`)

```python
# YANLIŞ: Hər 'item' üçün 'created_by' (User) cədvəlinə ayrıca sorğu gedəcək.
items = MyEntity.objects.all()
for item in items:
    print(item.created_by.get_full_name()) # N dənə əlavə sorğu

# DOĞRU: İki cədvəli SQL JOIN ilə birləşdirərək tək sorğuda gətirir.
items = MyEntity.objects.select_related('created_by').all()
for item in items:
    print(item.created_by.get_full_name()) # Cəmi 1 sorğu
```

### ManyToManyField və Reverse ForeignKey üçün (`prefetch_related`)

```python
# YANLIŞ: Hər 'campaign' üçün 'participants' cədvəlinə ayrıca sorğu gedəcək.
campaigns = EvaluationCampaign.objects.all()
for campaign in campaigns:
    print([p.username for p in campaign.participants.all()]) # N dənə əlavə sorğu

# DOĞRU: Bütün kampaniyalar üçün iştirakçıları 1 əlavə IN sorğusu ilə gətirir (Python tərəfində birləşdirir).
campaigns = EvaluationCampaign.objects.prefetch_related('participants').all()
for campaign in campaigns:
    print([p.username for p in campaign.participants.all()]) # Cəmi 2 sorğu (Biri campaigns, biri participants üçün)
```

### Gəlişmiş Prefetching (`Prefetch` obyekti)

```python
from django.db.models import Prefetch
from apps.accounts.models import User

# Yalnız aktiv iştirakçıları əvvəlcədən gətirir
active_participants_prefetch = Prefetch(
    'participants',
    queryset=User.objects.filter(is_active=True)
)

campaigns = EvaluationCampaign.objects.prefetch_related(active_participants_prefetch)
```

## 2. Gərəksiz Məlumatların Gətirilməməsi (`only` və `defer`)

Əgər modelin 20 sahəsi varsa, amma sənə yalnız 3-ü lazımdırsa, bütün məlumatı yaddaşa yükləmə.

```python
# YANLIŞ: Bütün sahələri gətirir
users = User.objects.all()

# DOĞRU: Yalnız ID, username və email sahələrini gətirir
users = User.objects.only('id', 'username', 'email')

# ALTERNATİV: description kimi böyük Text sahələrini (və ya JSONField-ləri) xaric et
items = MyEntity.objects.defer('large_json_data', 'long_description')
```

**DİQQƏT:** `only()` və `defer()` istifadə etdikdən sonra sənədləşdirilməyən (gətirilməyən) bir sahəni çağırsan, N+1 problemi yaradaraq hər obyekt üçün ayrıca sorğu atacaq.

## 3. Toplu Əməliyyatlar (Bulk Operations)

Loop daxilində tək-tək `save()` etmək ən böyük performans qatillərindən biridir.

### Toplu Yaratma (`bulk_create`)

```python
# YANLIŞ: N dənə INSERT sorğusu
for item_data in data_list:
    MyEntity.objects.create(**item_data)

# DOĞRU: Tək bir INSERT sorğusu
new_entities = [MyEntity(**item_data) for item_data in data_list]
MyEntity.objects.bulk_create(new_entities, batch_size=500)
```

### Toplu Yeniləmə (`bulk_update` və ya `update`)

```python
# Bütün uyğun qeydləri tək sorğuda yenilə
MyEntity.objects.filter(status='draft').update(status='active')

# Mövcud obyektlərin müəyyən sahələrini toplu yenilə
entities = MyEntity.objects.filter(category='A')
for entity in entities:
    entity.score += 10
MyEntity.objects.bulk_update(entities, ['score'])
```

## 4. Düzgün Hesablamalar (Annotation & Aggregation)

Hesablamaları Python yaddaşında deyil, birbaşa verilənlər bazasında et.

```python
from django.db.models import Count, Sum, Avg, F, Q

# YANLIŞ: Hər kampaniyanın iştirakçı sayını tapmaq
campaigns = EvaluationCampaign.objects.all()
for c in campaigns:
    count = c.participants.count() # N+1 sorğu

# DOĞRU: SQL tərəfində COUNT et
campaigns = EvaluationCampaign.objects.annotate(participant_count=Count('participants'))
for c in campaigns:
    count = c.participant_count # 1 sorğu

# Aggregation (Bütün cədvəl üzrə ümumi statistika)
stats = EvaluationResult.objects.aggregate(
    total_score=Sum('score'),
    average_score=Avg('score'),
    completed_count=Count('id', filter=Q(status='completed')) # Düzgün şərtli Count
)
```

## 5. İndekslərin (Indexes) Əlavə Edilməsi

Çox axtarılan, filtrlənən (filter/exclude) və sıralanan (order_by) sahələr indekslənməlidir.

```python
class EvaluationCampaign(models.Model):
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    start_date = models.DateField()
    
    class Meta:
        indexes = [
            # Tez-tez statusa və başlanğıc tarixinə görə axtarışlar üçün
            models.Index(fields=['status', 'start_date']),
            
            # Gəlişmiş axtarış (GinIndex PostgreSQL üçün)
            # from django.contrib.postgres.indexes import GinIndex
            # GinIndex(fields=['search_vector'])
        ]
```

## 6. QuerySet-in Keşlənməsi və Qiymətləndirilməsi

QuerySet-lər "lazy" (tənbəl) işləyir. Cədvəli 2 dəfə çağırmamaq üçün dəyişəndə saxla.

```python
# YANLIŞ: 2 sorğu gedəcək
if items.exists():
    for item in items:
        pass

# DOĞRU: `list()` istifadə edərək 1 dəfə yüklə (Əgər məlumat çox deyilsə)
items_list = list(items)
if items_list:
    for item in items_list:
        pass

# Yalnız mövcudluq yoxlaması:
if items.exists(): # Sadəcə LIMIT 1 sorğusu atır
    print("Mövcuddur")
```

## 7. Development (İnkişaf) Zamanı Yoxlama

N+1 sorğularını inkişaf zamanı aşkar etmək üçün:

1. **Django Debug Toolbar**: `settings.DEBUG = True` olanda SQL paneli N+1-ləri göstərir.
2. **Sorğu Sayını Print Etmək**:
```python
from django.db import connection
print(f"Sorğu sayı: {len(connection.queries)}")
```
3. Docker mühitində audit scripti: `docker compose exec web python show_dup_queries.py /<page-url>/`
