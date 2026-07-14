---
name: django-modul-yarat
description: >
  Q360 layihəsində yeni Django modulu (app) yaratmaq üçün uçdan-uca bələdçi. Model, view,
  serializer, URL, template, migration və admin qeydiyyatını layihə konvensiyalarına tam uyğun
  şəkildə yaradır. Tetikleyicilər: "yeni modul yarat", "yeni app əlavə et", "bu modulu tik",
  "batch X-i tik", "yeni səhifə yarat", "CRUD yarat", "yeni feature əlavə et", "bu endpoint-i
  yarat", "new module", "create app". Claude.md-dəki Batch tikinti planını yerinə yetirərkən
  bu skill-i istifadə et.
---

# Django Modul Yaratma — Q360 Konvensiyasına Uyğun

Bu skill Q360 layihəsində yeni Django modulu yaratmaq üçün tam axışı izah edir.
`q360-konvensiya` skill-indəki bütün qaydalara əməl etmək MƏCBURİDİR.

## Yaratmadan ƏVVƏL (Məcburi Yoxlama)

1. Mövcud 2-3 tam modulu (məs. `apps/evaluations/`, `apps/leave_attendance/`) oxu:
   - `models.py` strukturu
   - `template_views.py` pattern-i
   - `serializers.py` (DRF istifadəsi)
   - `urls.py` qeydiyyat pattern-i
   - Template strukturu
2. `apps/core/models.py`-dəki `TimeStampedModel` və `SoftDeletableModel`-i bil
3. `config/urls.py`-dəki URL qeydiyyat pattern-ini bil

## Addım-addım Axış

### Addım 1: App Strukturu Yaratma

```
apps/<app_name>/
├── __init__.py
├── admin.py           # django-unfold admin qeydiyyatı
├── apps.py            # AppConfig
├── forms.py           # Django forms (template views üçün)
├── models.py          # Data models
├── serializers.py     # DRF serializers
├── signals.py         # Siqnallar (lazım olduqda)
├── tasks.py           # Celery tasks (lazım olduqda)
├── template_views.py  # Template-based views (HTML səhifələr)
├── views.py           # API views (DRF ViewSets)
├── urls.py            # URL routing
├── tests/
│   ├── __init__.py
│   └── test_views.py
└── migrations/
    └── __init__.py
```

### Addım 2: apps.py

```python
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MyModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.my_module'
    verbose_name = _('Modul Adı')

    def ready(self):
        try:
            from . import signals  # noqa: F401
        except ImportError:
            pass
```

### Addım 3: models.py

```python
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from apps.core.models import TimeStampedModel


class MyEntity(TimeStampedModel):
    """Qısa təsvir."""

    STATUS_CHOICES = [
        ('draft', _('Qaralama')),
        ('active', _('Aktiv')),
        ('completed', _('Tamamlanmış')),
        ('archived', _('Arxivlənmiş')),
    ]

    title = models.CharField(max_length=200, verbose_name=_('Başlıq'))
    description = models.TextField(blank=True, verbose_name=_('Təsvir'))
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='draft',
        verbose_name=_('Status')
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='my_entities',
        verbose_name=_('Yaradan')
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Obyekt Adı')
        verbose_name_plural = _('Obyekt Adları')

    def __str__(self):
        return self.title
```

### Addım 4: template_views.py

```python
"""Template-based views for my_module app."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _

from .models import MyEntity
from .forms import MyEntityForm


class MyEntityListView(LoginRequiredMixin, ListView):
    model = MyEntity
    template_name = 'my_module/list.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        queryset = MyEntity.objects.select_related('created_by')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by('-created_at')


class MyEntityDetailView(LoginRequiredMixin, DetailView):
    model = MyEntity
    template_name = 'my_module/detail.html'
    context_object_name = 'item'


class MyEntityCreateView(LoginRequiredMixin, CreateView):
    model = MyEntity
    form_class = MyEntityForm
    template_name = 'my_module/form.html'
    success_url = reverse_lazy('my_module:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, _('Uğurla yaradıldı.'))
        return super().form_valid(form)


class MyEntityUpdateView(LoginRequiredMixin, UpdateView):
    model = MyEntity
    form_class = MyEntityForm
    template_name = 'my_module/form.html'
    success_url = reverse_lazy('my_module:list')

    def form_valid(self, form):
        messages.success(self.request, _('Uğurla yeniləndi.'))
        return super().form_valid(form)


@login_required
def my_entity_delete(request, pk):
    item = get_object_or_404(MyEntity, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, _('Uğurla silindi.'))
        return redirect('my_module:list')
    return render(request, 'my_module/confirm_delete.html', {'item': item})
```

### Addım 5: urls.py

```python
from django.urls import path
from . import template_views

app_name = 'my_module'

urlpatterns = [
    path('', template_views.MyEntityListView.as_view(), name='list'),
    path('create/', template_views.MyEntityCreateView.as_view(), name='create'),
    path('<int:pk>/', template_views.MyEntityDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', template_views.MyEntityUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', template_views.my_entity_delete, name='delete'),
]
```

### Addım 6: forms.py

```python
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import MyEntity


class MyEntityForm(forms.ModelForm):
    class Meta:
        model = MyEntity
        fields = ['title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border-gray-300 dark:border-gray-600 '
                         'dark:bg-gray-700 dark:text-white focus:ring-indigo-500',
                'placeholder': _('Başlıq daxil edin')
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border-gray-300 dark:border-gray-600 '
                         'dark:bg-gray-700 dark:text-white focus:ring-indigo-500',
                'rows': 4,
                'placeholder': _('Təsvir daxil edin')
            }),
            'status': forms.Select(attrs={
                'class': 'w-full rounded-lg border-gray-300 dark:border-gray-600 '
                         'dark:bg-gray-700 dark:text-white focus:ring-indigo-500'
            }),
        }
```

### Addım 7: serializers.py (API üçün)

```python
from rest_framework import serializers
from .models import MyEntity


class MyEntitySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source='created_by.get_full_name', read_only=True
    )

    class Meta:
        model = MyEntity
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']
```

### Addım 8: views.py (API ViewSet)

```python
from rest_framework import viewsets, permissions
from .models import MyEntity
from .serializers import MyEntitySerializer


class MyEntityViewSet(viewsets.ModelViewSet):
    queryset = MyEntity.objects.select_related('created_by').all()
    serializer_class = MyEntitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
```

### Addım 9: admin.py

```python
from django.contrib import admin
from unfold.admin import ModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import MyEntity


@admin.register(MyEntity)
class MyEntityAdmin(ModelAdmin, SimpleHistoryAdmin):
    list_display = ['title', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
```

### Addım 10: Template-lər

Template-lər `templates/<app_name>/` qovluğunda yaradılmalıdır.
Bütün template-lər `{% extends "base/base.html" %}` ilə başlamalıdır.
TailwindCSS class-ları ilə stilləndirmə.
Responsive dizayn (375px/768px/1440px).
i18n: bütün statik mətnlər `{% trans %}` ilə sarılmalıdır.

### Addım 11: Qeydiyyat

1. **INSTALLED_APPS**-a əlavə et (`config/settings.py`):
   ```python
   'apps.my_module',
   ```

2. **Root URL-ə əlavə et** (`config/urls.py`):
   ```python
   path('my-module/', include('apps.my_module.urls', namespace='my_module')),
   ```

3. **API URL-ə əlavə et** (`config/api_urls.py`) — lazım olduqda:
   ```python
   router.register(r'my-module', MyEntityViewSet, basename='my-module')
   ```

4. **Sidebar-a əlavə et** (`templates/base/sidebar.html`) — naviqasiya linki

### Addım 12: Yoxlama (Məcburi)

```bash
# Migration yaratma
python manage.py makemigrations my_module

# Migration tətbiqi
python manage.py migrate

# System check
python manage.py check

# Səhifə yoxlaması (200 status gözlənilir)
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/my-module/
```

## SUPERUSER-ONLY Modullar üçün Əlavə Qaydalar

Superuser-only modullar (admin, system, files, ai) üçün:
- Sidebar-da ayrı bölmədə göstər
- View-larda `user.is_superuser` yoxlaması əlavə et
- Adi istifadəçi naviqasiyasında GÖRÜNMƏMƏLİDİR

## STUB/Coming Soon Modullar üçün

Real inteqrasiya tələb edən modullar (MFA, SSO, Workflow Designer, Policy Simulator) üçün:
- UI skeleton yaradılmalıdır
- "Tezliklə" (Coming Soon) statusu göstərilməlidir
- TODO comment əlavə olunmalıdır
- Jurnalda "real spec tələb edir" qeydi olmalıdır
