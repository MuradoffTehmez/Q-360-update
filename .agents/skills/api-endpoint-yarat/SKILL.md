---
name: api-endpoint-yarat
description: >
  Q360 layihəsində DRF (Django REST Framework) API endpoint yaratmaq, genişləndirmək və ya
  debug etmək üçün uçdan-uca bələdçi. ViewSet, Serializer, URL routing, permission,
  throttling, pagination, filtering və drf-spectacular schema konfiqurasiyasını layihə
  konvensiyalarına uyğun yaradır. Tetikleyicilər: "API yarat", "endpoint əlavə et",
  "API yaz", "REST endpoint", "ViewSet yarat", "serializer yaz", "API debug et",
  "Postman collection yenilə", "swagger-a əlavə et", "create API", "add endpoint".
---

# API Endpoint Yaratma — Q360 DRF Konvensiyası

Bu skill Q360 layihəsində DRF API endpoint-ləri yaratmaq və idarə etmək üçün tam axışı izah edir.
Bütün API-lər `/api/v1/` prefix altında, `config/api_urls.py`-da qeydiyyat olunur.

## API Arxitektura Qaydaları

### URL Strukturu

```
/api/v1/<module>/                    → List + Create
/api/v1/<module>/<id>/               → Retrieve + Update + Delete
/api/v1/<module>/<id>/<action>/      → Custom actions
```

### Autentifikasiya

- JWT (SimpleJWT) — `Authorization: Bearer <token>`
- Token əldə: `POST /api/auth/token/`
- Token yenilə: `POST /api/auth/token/refresh/`
- Token yoxla: `POST /api/auth/token/verify/`

### Throttling

```python
# settings.py-da qlobal
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/min',
        'user': '100/min',
    }
}
```

## Tam Endpoint Yaratma Axışı

### 1. Model (əgər yoxdursa)

`q360-konvensiya` və `django-modul-yarat` skill-lərinə bax.

### 2. Serializer

```python
# apps/<module>/serializers.py

from rest_framework import serializers
from .models import MyEntity


class MyEntityListSerializer(serializers.ModelSerializer):
    """Siyahı üçün yüngül serializer."""
    created_by_name = serializers.CharField(
        source='created_by.get_full_name', read_only=True
    )

    class Meta:
        model = MyEntity
        fields = ['id', 'title', 'status', 'created_by_name', 'created_at']


class MyEntityDetailSerializer(serializers.ModelSerializer):
    """Detallı serializer — tam sahələr."""
    created_by_name = serializers.CharField(
        source='created_by.get_full_name', read_only=True
    )

    class Meta:
        model = MyEntity
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Başlıq minimum 3 simvol olmalıdır.')
        return value
```

### 3. ViewSet

```python
# apps/<module>/views.py

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import MyEntity
from .serializers import MyEntityListSerializer, MyEntityDetailSerializer


@extend_schema_view(
    list=extend_schema(summary='Siyahı', tags=['My Module']),
    retrieve=extend_schema(summary='Detallar', tags=['My Module']),
    create=extend_schema(summary='Yarat', tags=['My Module']),
    update=extend_schema(summary='Yenilə', tags=['My Module']),
    destroy=extend_schema(summary='Sil', tags=['My Module']),
)
class MyEntityViewSet(viewsets.ModelViewSet):
    """MyEntity CRUD API."""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'created_by']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        return MyEntity.objects.select_related('created_by').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return MyEntityListSerializer
        return MyEntityDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @extend_schema(summary='Status dəyiş', tags=['My Module'])
    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None):
        item = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(MyEntity.STATUS_CHOICES):
            return Response(
                {'error': 'Yanlış status'},
                status=status.HTTP_400_BAD_REQUEST
            )
        item.status = new_status
        item.save(update_fields=['status'])
        return Response(MyEntityDetailSerializer(item).data)
```

### 4. URL Qeydiyyatı

```python
# config/api_urls.py-da əlavə et:

from apps.my_module.views import MyEntityViewSet

router.register(r'my-module', MyEntityViewSet, basename='my-module')
```

### 5. Swagger/Redoc Schema

drf-spectacular avtomatik olaraq schema yaradır.
`@extend_schema` decorator-unu istifadə edərək əlavə metadata əlavə et.

Swagger UI: `http://localhost:8000/api/schema/swagger-ui/`
Redoc: `http://localhost:8000/api/schema/redoc/`

### 6. Test

```python
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User


class MyEntityAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testapi', password='test123'
        )
        self.client.force_authenticate(user=self.user)

    def test_list(self):
        url = reverse('my-module-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = reverse('my-module-list')
        data = {'title': 'Test', 'description': 'Desc', 'status': 'draft'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

## Response Formatı Standartı

Uğurlu cavab:
```json
{
  "count": 42,
  "next": "http://localhost:8000/api/v1/my-module/?page=2",
  "previous": null,
  "results": [...]
}
```

Xəta cavabı:
```json
{
  "detail": "Authentication credentials were not provided.",
  "code": "not_authenticated"
}
```

## Pagination

DRF-in default `PageNumberPagination`-ı istifadə olunur.
`page_size = 20` qlobal olaraq `settings.py`-da təyin olunub.

## Postman Collection

Yeni endpoint əlavə etdikdə, Postman collection-ı yeniləmək üçün:

```bash
python generate_postman.py
```

Bu `Q360_Full_API.postman_collection.json` faylını yenidən yaradır.

## API Versiyalama

Bütün API-lər `/api/v1/` altındadır. Gələcəkdə v2 lazım olarsa,
`config/api_urls_v2.py` yaradılacaq.
