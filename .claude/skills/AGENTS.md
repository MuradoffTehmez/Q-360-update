# Q360 — Layihə Qaydaları

## Dil

- Kod kommentləri: İngiliscə və ya Azərbaycanca (mövcud kodun dilinə uyğunlaş)
- Model verbose_name: Azərbaycanca, `gettext_lazy` ilə
- Template mətnlər: `{% trans %}` ilə sarılmış Azərbaycanca
- Git commit mesajları: İngiliscə
- İstifadəçi ilə ünsiyyət: Azərbaycanca

## Kod Stili

- Python: PEP 8
- Indent: 4 boşluq (Python), 2 boşluq (HTML/CSS/JS)
- Line length: 120 simvol (Python)
- Import sırası: stdlib → third-party → Django → local apps
- String-lər: single quote (Python), double quote (HTML atributları)

## Vacib Qaydalar

1. **Heç vaxt** `.env` faylını git-ə commit etmə
2. **Hər zaman** `select_related()` / `prefetch_related()` istifadə et (N+1 qarşısı)
3. **Hər zaman** `LoginRequiredMixin` / `@login_required` istifadə et
4. **Hər zaman** migration yaratdıqdan sonra `manage.py check` icra et
5. **Heç vaxt** inline CSS / inline JS istifadə etmə (mümkün qədər)
6. **Hər zaman** dark mode dəstəyi əlavə et (`dark:` prefix)
7. **Hər zaman** responsive dizayn təmin et (375px / 768px / 1440px)
8. **Heç vaxt** hardcoded Azərbaycan mətni istifadə etmə — `{% trans %}` ilə sarıl

## Branch Strategiyası

- `main` — production-ready kod
- `develop` — development branch
- Feature branch-lar: `feature/<modul-adi>` formatında

## Commit Mesaj Formatı

```
<type>(<scope>): <description>

Nümunə:
feat(evaluations): add calibration dashboard
fix(accounts): resolve N+1 query in profile view
refactor(templates): extract sidebar into component
```
