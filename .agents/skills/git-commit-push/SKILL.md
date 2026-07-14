---
name: git-commit-push
description: >
  Q360 layihəsində hər hansı bir modul dəyişikliyi, yeni feature (batch) tikintisi və ya 
  task bitdikdən sonra kodu avtomatik olaraq detallı şəkildə Git-ə commit edib yükləmək (push) 
  üçün bələdçi. Conventional Commits standartlarına uyğun detallı commit mesajı formatını müəyyən edir.
  Tetikleyicilər: "git-ə yüklə", "commit et", "push et", "kodu yadda saxla", "save changes",
  "işi bitirdim, gitə at", "git commit and push", "commit yaz".
---

# Git Commit və Push İş Axışı — Q360

Bu skill layihədəki hər hansı bir dəyişikliyin, yeni səhifənin, bug fix-in və ya batch-in 
tamamlanmasından sonra agentin (mənim və ya Claude-un) kodu Git-ə düzgün şəkildə necə 
göndərəcəyini müəyyən edir. 

Hər bir işin sonunda əgər istifadəçi razıdırsa (yaxud avtomatik iş axışındadırsa), mütləq
şəkildə bu qaydalara əsaslanaraq kodu commit və push etmək lazımdır.

## 1. Commit Etmədən Əvvəl Yoxlama

Kodu git-ə yükləməmişdən əvvəl həmişə bu yoxlamanı sürətli şəkildə et:
1. `git status` ilə yalnız aidiyyatı olan dəyişikliklərin edildiyindən əmin ol.
2. Səhvən `.env`, `__pycache__/` və ya məlumat bazası (`.sqlite3`) faylları əlavə olunmayıbsa əmin ol.

## 2. Commit Mesaj Formatı (Conventional Commits)

Commit mesajları İNGİLİS dilində yazılmalı və aşağıdakı struktura sahib olmalıdır. Mesaj "detailed" (detallı) olmalıdır, sadəcə 1 cümləlik deyil, həm başlığı, həm də görülən işlərin siyahısını özündə cəmləşdirməlidir.

**Format:**
```
<type>(<scope>): <qısa təsvir (max 50 simvol)>

<Detallı izah: Problemin nə idi və necə həll edildi. Hansı yeni fayllar əlavə edildi.>
- <Görülən iş 1>
- <Görülən iş 2>
- <Görülən iş 3>
```

**Tiplər (<type>):**
- `feat`: Yeni bir xüsusiyyət (feature) və ya modul əlavə edildikdə (məsələn, yeni səhifə).
- `fix`: Xəta (bug) düzəldildikdə.
- `refactor`: Mövcud kodun strukturunda dəyişiklik edildikdə (funksionallıq dəyişmədən).
- `style`: Formatlama (CSS, Tailwind) və vizual dəyişikliklər.
- `docs`: Sənədləşdirmə, skill-lər və ya README dəyişiklikləri.
- `chore`: Paket yenilənməsi, konfiqurasiya dəyişiklikləri (Docker, requirements.txt).

**Əhatə (<scope>):**
Dəyişikliyin aid olduğu modul və ya qovluq (məsələn: `evaluations`, `auth`, `ui`, `celery`, `skills`).

### Mükəmməl Commit Nümunəsi:

```text
feat(settings): implement complete settings module (Batch 1)

Added 23 new pages for the settings module including general,
localization, security, and notification preferences.

- Created Settings BaseModel and specific configuration models
- Implemented class-based views with RBAC protection
- Added Tailwind CSS styled templates with dark mode support
- Created STUB pages for MFA and SSO integrations
- Registered all new URLs in the main router
```

## 3. İcra Ediləcək Komandalar

Agent işi bitirdikdə birbaşa aşağıdakı komandaları icra etməlidir:

```bash
# 1. Bütün dəyişiklikləri əlavə et
git add .

# 2. Detallı commit mesajı ilə commit et
# DİQQƏT: Çoxsətirli mesaj üçün -m parametrini iki dəfə istifadə edə bilərsiniz, 
# yaxud echo ilə birbaşa git commit-ə yönləndirə bilərsiniz.

git commit -m "feat(module_name): short description" -m "Detailed explanation of changes:
- Item 1
- Item 2"

# 3. Kodu uzaq serverə (GitHub/GitLab/Bitbucket) push et
git push origin <cari_branch>
```

## 4. Claude Code və Antigravity üçün Təlimat

- **Avtomatlaşdırma:** Hər hansı "Batch X" tikintisi (məsələn `batch-tikinti` qaydası ilə) bitdikdən sonra agent istifadəçiyə bildirməlidir: *"Dəyişikliklər tamamlandı, indi kodu Git-ə commit və push edirəm."* və icra etməlidir.
- **Detallar:** Commit mesajındakı bullet-point-lərdə (siyahıda) real olaraq dəyişdirilən fayllar (məsələn: `models.py updated`, `new list.html created`) haqqında mütləq bilgi olmalıdır.
