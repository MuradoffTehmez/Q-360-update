---
name: sehife-yarat
description: >
  Q360 layihəsində tam funksional yeni səhifə yaratmaq üçün uçdan-uca skill. List, Detail,
  Create/Edit Form, Delete Confirmation, Dashboard widget, Settings, Report və STUB səhifə
  tiplərini əhatə edir. Hər tip üçün real template nümunələri, sidebar qeydiyyatı, breadcrumb,
  pagination, filter, empty state, statistika kartları, action düymələri, modal dialogs, dark
  mode, responsive dizayn daxildir. Tetikleyicilər: "yeni səhifə yarat", "list səhifəsi",
  "detail səhifəsi", "form səhifəsi", "CRUD səhifələri", "template yarat", "dashboard widget",
  "settings səhifəsi", "report səhifəsi", "səhifə əlavə et", "UI yarat", "create page",
  "add page", "build page", "new page".
---

# Tam Funksional Səhifə Yaratma — Q360

Bu skill Q360 layihəsində müxtəlif tipli səhifələr yaratmaq üçün tam boilerplate template-lər
və real kod nümunələri təqdim edir.

## Səhifə Tipləri

1. **List Səhifəsi** — Cədvəl + filter + axtarış + pagination + statistika kartları
2. **Detail Səhifəsi** — Obyekt detalları + əlaqəli data + action düymələr
3. **Form Səhifəsi** — Create/Edit formu + validation + success mesajları
4. **Delete Confirmation** — Silmə təsdiqi modal/səhifəsi
5. **Dashboard/Widget Səhifəsi** — KPI kartları + Chart.js qrafiklər
6. **Settings Səhifəsi** — Tab-lı parametrlər paneli
7. **Report Səhifəsi** — Filter + cədvəl + export (PDF/Excel)
8. **STUB/Coming Soon** — Gələcək funksionallıq üçün placeholder

---

## 1. List Səhifəsi (Tam Template)

### View (template_views.py)

```python
class MyEntityListView(LoginRequiredMixin, ListView):
    """List all entities with search, filter and statistics."""
    model = MyEntity
    template_name = 'my_module/list.html'
    context_object_name = 'items'
    paginate_by = 10

    def get_queryset(self):
        queryset = MyEntity.objects.select_related('created_by', 'category')

        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Status filter
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Date range filter
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        if date_from:
            queryset = queryset.filter(created_at__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__date__lte=date_to)

        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aggregate statistikalar (tək query ilə)
        stats = MyEntity.objects.aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(status='active')),
            draft=Count('id', filter=Q(status='draft')),
            completed=Count('id', filter=Q(status='completed')),
        )
        context.update(stats)
        return context
```

### Template (templates/my_module/list.html)

```html
{% extends 'base/base.html' %}
{% load static i18n %}

{% block title %}{% trans "Siyahı" %} - Q360{% endblock %}

{% block page_header %}
<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
    <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
            <i class="fas fa-list-alt text-indigo-500 mr-2"></i>
            {% trans "Modul Adı" %}
        </h1>
        <p class="text-gray-500 dark:text-gray-400 mt-1">{% trans "Bütün elementlərin siyahısı" %}</p>
    </div>
    {% if user.is_admin %}
    <a href="{% url 'my_module:create' %}"
       class="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white
              font-medium rounded-lg shadow-sm transition-colors duration-200">
        <i class="fas fa-plus mr-2"></i>
        {% trans "Yeni Əlavə Et" %}
    </a>
    {% endif %}
</div>
{% endblock %}

{% block content %}
<!-- Statistika Kartları -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200
                dark:border-gray-700 p-5 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
            <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">{% trans "Toplam" %}</p>
                <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ total }}</p>
            </div>
            <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center
                        justify-center">
                <i class="fas fa-layer-group text-blue-600 dark:text-blue-400"></i>
            </div>
        </div>
    </div>
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200
                dark:border-gray-700 p-5 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
            <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">{% trans "Aktiv" %}</p>
                <p class="text-2xl font-bold text-green-600 dark:text-green-400">{{ active }}</p>
            </div>
            <div class="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center
                        justify-center">
                <i class="fas fa-check-circle text-green-600 dark:text-green-400"></i>
            </div>
        </div>
    </div>
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200
                dark:border-gray-700 p-5 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
            <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">{% trans "Qaralama" %}</p>
                <p class="text-2xl font-bold text-amber-600 dark:text-amber-400">{{ draft }}</p>
            </div>
            <div class="w-12 h-12 bg-amber-100 dark:bg-amber-900/30 rounded-full flex items-center
                        justify-center">
                <i class="fas fa-file-alt text-amber-600 dark:text-amber-400"></i>
            </div>
        </div>
    </div>
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200
                dark:border-gray-700 p-5 hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between">
            <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">{% trans "Tamamlanmış" %}</p>
                <p class="text-2xl font-bold text-purple-600 dark:text-purple-400">{{ completed }}</p>
            </div>
            <div class="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-full flex items-center
                        justify-center">
                <i class="fas fa-trophy text-purple-600 dark:text-purple-400"></i>
            </div>
        </div>
    </div>
</div>

<!-- Filter Panel -->
<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200
            dark:border-gray-700 p-5 mb-6">
    <form method="get" class="grid grid-cols-1 md:grid-cols-4 gap-4"
          data-ajax-filter data-ajax-target="#results-table">
        <div>
            <input type="text" name="search" value="{{ request.GET.search }}"
                   class="w-full rounded-lg border-gray-300 dark:border-gray-600
                          dark:bg-gray-700 dark:text-white focus:ring-indigo-500
                          focus:border-indigo-500"
                   placeholder="{% trans 'Axtar...' %}">
        </div>
        <div>
            <select name="status"
                    class="w-full rounded-lg border-gray-300 dark:border-gray-600
                           dark:bg-gray-700 dark:text-white focus:ring-indigo-500">
                <option value="">{% trans "Bütün Statuslar" %}</option>
                <option value="draft" {% if request.GET.status == 'draft' %}selected{% endif %}>
                    {% trans "Qaralama" %}
                </option>
                <option value="active" {% if request.GET.status == 'active' %}selected{% endif %}>
                    {% trans "Aktiv" %}
                </option>
                <option value="completed" {% if request.GET.status == 'completed' %}selected{% endif %}>
                    {% trans "Tamamlanmış" %}
                </option>
            </select>
        </div>
        <div class="flex gap-2">
            <button type="submit"
                    class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-medium
                           py-2 px-4 rounded-lg transition-colors">
                <i class="fas fa-filter mr-1"></i> {% trans "Filtr" %}
            </button>
            <a href="{% url 'my_module:list' %}"
               class="flex-1 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600
                      text-gray-700 dark:text-gray-300 font-medium py-2 px-4 rounded-lg
                      transition-colors text-center">
                <i class="fas fa-redo mr-1"></i> {% trans "Sıfırla" %}
            </a>
        </div>
    </form>
</div>

<!-- Nəticə Cədvəli -->
<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200
            dark:border-gray-700 overflow-hidden" id="results-table">
    {% if items %}
    <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-900/50">
                <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500
                               dark:text-gray-400 uppercase tracking-wider">
                        {% trans "Başlıq" %}
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500
                               dark:text-gray-400 uppercase tracking-wider">
                        {% trans "Status" %}
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500
                               dark:text-gray-400 uppercase tracking-wider">
                        {% trans "Yaradan" %}
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500
                               dark:text-gray-400 uppercase tracking-wider">
                        {% trans "Tarix" %}
                    </th>
                    <th class="px-6 py-3 text-right text-xs font-medium text-gray-500
                               dark:text-gray-400 uppercase tracking-wider">
                        {% trans "Əməliyyatlar" %}
                    </th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                {% for item in items %}
                <tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                    <td class="px-6 py-4">
                        <div class="flex items-center">
                            <div class="w-10 h-10 bg-indigo-100 dark:bg-indigo-900/30 rounded-full
                                        flex items-center justify-center mr-3">
                                <i class="fas fa-file-alt text-indigo-600 dark:text-indigo-400"></i>
                            </div>
                            <div>
                                <a href="{% url 'my_module:detail' item.pk %}"
                                   class="font-medium text-gray-900 dark:text-white
                                          hover:text-indigo-600 dark:hover:text-indigo-400">
                                    {{ item.title }}
                                </a>
                                {% if item.description %}
                                <p class="text-sm text-gray-500 dark:text-gray-400 truncate max-w-xs">
                                    {{ item.description|truncatewords:8 }}
                                </p>
                                {% endif %}
                            </div>
                        </div>
                    </td>
                    <td class="px-6 py-4">
                        {% if item.status == 'active' %}
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs
                                     font-medium bg-green-100 text-green-800
                                     dark:bg-green-900/30 dark:text-green-400">
                            <span class="w-1.5 h-1.5 bg-green-500 rounded-full mr-1.5"></span>
                            {% trans "Aktiv" %}
                        </span>
                        {% elif item.status == 'draft' %}
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs
                                     font-medium bg-amber-100 text-amber-800
                                     dark:bg-amber-900/30 dark:text-amber-400">
                            <span class="w-1.5 h-1.5 bg-amber-500 rounded-full mr-1.5"></span>
                            {% trans "Qaralama" %}
                        </span>
                        {% elif item.status == 'completed' %}
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs
                                     font-medium bg-blue-100 text-blue-800
                                     dark:bg-blue-900/30 dark:text-blue-400">
                            <span class="w-1.5 h-1.5 bg-blue-500 rounded-full mr-1.5"></span>
                            {% trans "Tamamlanmış" %}
                        </span>
                        {% endif %}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {{ item.created_by.get_full_name|default:"-" }}
                    </td>
                    <td class="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {{ item.created_at|date:"d.m.Y H:i" }}
                    </td>
                    <td class="px-6 py-4 text-right">
                        <div class="flex items-center justify-end space-x-2">
                            <a href="{% url 'my_module:detail' item.pk %}"
                               class="p-2 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30
                                      rounded-lg transition-colors" title="{% trans 'Bax' %}">
                                <i class="fas fa-eye"></i>
                            </a>
                            {% if user.is_admin %}
                            <a href="{% url 'my_module:edit' item.pk %}"
                               class="p-2 text-amber-600 hover:bg-amber-50 dark:hover:bg-amber-900/30
                                      rounded-lg transition-colors" title="{% trans 'Redaktə' %}">
                                <i class="fas fa-edit"></i>
                            </a>
                            <a href="{% url 'my_module:delete' item.pk %}"
                               class="p-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/30
                                      rounded-lg transition-colors" title="{% trans 'Sil' %}">
                                <i class="fas fa-trash"></i>
                            </a>
                            {% endif %}
                        </div>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <!-- Pagination -->
    {% if is_paginated %}
    <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
            <p class="text-sm text-gray-500 dark:text-gray-400">
                {% trans "Səhifə" %} {{ page_obj.number }} / {{ page_obj.paginator.num_pages }}
                ({% trans "toplam" %} {{ page_obj.paginator.count }} {% trans "nəticə" %})
            </p>
            <nav class="flex items-center space-x-1">
                {% if page_obj.has_previous %}
                <a href="?page=1{% if request.GET.search %}&search={{ request.GET.search }}{% endif %}"
                   class="px-3 py-2 text-sm rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                    <i class="fas fa-angle-double-left"></i>
                </a>
                <a href="?page={{ page_obj.previous_page_number }}"
                   class="px-3 py-2 text-sm rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                    <i class="fas fa-angle-left"></i>
                </a>
                {% endif %}
                <span class="px-3 py-2 text-sm bg-indigo-600 text-white rounded-lg">
                    {{ page_obj.number }}
                </span>
                {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}"
                   class="px-3 py-2 text-sm rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                    <i class="fas fa-angle-right"></i>
                </a>
                <a href="?page={{ page_obj.paginator.num_pages }}"
                   class="px-3 py-2 text-sm rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                    <i class="fas fa-angle-double-right"></i>
                </a>
                {% endif %}
            </nav>
        </div>
    </div>
    {% endif %}

    {% else %}
    <!-- Empty State -->
    <div class="flex flex-col items-center justify-center py-16 px-4">
        <div class="w-20 h-20 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center
                    justify-center mb-4">
            <i class="fas fa-inbox text-3xl text-gray-400 dark:text-gray-500"></i>
        </div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            {% trans "Nəticə tapılmadı" %}
        </h3>
        <p class="text-gray-500 dark:text-gray-400 mb-6 text-center max-w-sm">
            {% trans "Hələ heç bir element yaradılmayıb." %}
        </p>
        {% if user.is_admin %}
        <a href="{% url 'my_module:create' %}"
           class="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700
                  text-white font-medium rounded-lg transition-colors">
            <i class="fas fa-plus mr-2"></i>
            {% trans "İlk Elementi Yarat" %}
        </a>
        {% endif %}
    </div>
    {% endif %}
</div>
{% endblock %}
```

---

## 2. Detail Səhifəsi Template

```html
{% extends 'base/base.html' %}
{% load static i18n %}

{% block title %}{{ item.title }} - Q360{% endblock %}

{% block content %}
<!-- Header -->
<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
    <div class="flex items-center space-x-4">
        <a href="{% url 'my_module:list' %}"
           class="p-2 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300
                  hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
            <i class="fas fa-arrow-left"></i>
        </a>
        <div>
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">{{ item.title }}</h1>
            <div class="flex items-center space-x-3 mt-1">
                <!-- Status Badge -->
                {% if item.status == 'active' %}
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs
                             font-medium bg-green-100 text-green-800
                             dark:bg-green-900/30 dark:text-green-400">
                    {% trans "Aktiv" %}
                </span>
                {% endif %}
                <span class="text-sm text-gray-500 dark:text-gray-400">
                    {{ item.created_at|date:"d.m.Y H:i" }}
                </span>
            </div>
        </div>
    </div>
    {% if user.is_admin %}
    <div class="flex items-center space-x-2">
        <a href="{% url 'my_module:edit' item.pk %}"
           class="inline-flex items-center px-4 py-2 bg-amber-500 hover:bg-amber-600
                  text-white font-medium rounded-lg transition-colors">
            <i class="fas fa-edit mr-2"></i> {% trans "Redaktə Et" %}
        </a>
        <a href="{% url 'my_module:delete' item.pk %}"
           class="inline-flex items-center px-4 py-2 bg-red-500 hover:bg-red-600
                  text-white font-medium rounded-lg transition-colors">
            <i class="fas fa-trash mr-2"></i> {% trans "Sil" %}
        </a>
    </div>
    {% endif %}
</div>

<!-- Detallar Grid -->
<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Əsas Məlumatlar -->
    <div class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl shadow-sm border
                border-gray-200 dark:border-gray-700 p-6">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            <i class="fas fa-info-circle text-blue-500 mr-2"></i>
            {% trans "Əsas Məlumatlar" %}
        </h2>
        <dl class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
                <dt class="text-sm text-gray-500 dark:text-gray-400">{% trans "Başlıq" %}</dt>
                <dd class="mt-1 text-gray-900 dark:text-white font-medium">{{ item.title }}</dd>
            </div>
            <div>
                <dt class="text-sm text-gray-500 dark:text-gray-400">{% trans "Status" %}</dt>
                <dd class="mt-1">{{ item.get_status_display }}</dd>
            </div>
            <div class="sm:col-span-2">
                <dt class="text-sm text-gray-500 dark:text-gray-400">{% trans "Təsvir" %}</dt>
                <dd class="mt-1 text-gray-900 dark:text-white">
                    {{ item.description|default:"-"|linebreaksbr }}
                </dd>
            </div>
        </dl>
    </div>

    <!-- Metadata Sidebar -->
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border
                border-gray-200 dark:border-gray-700 p-6">
        <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            <i class="fas fa-clock text-gray-500 mr-2"></i>
            {% trans "Metadata" %}
        </h2>
        <div class="space-y-4">
            <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">{% trans "Yaradan" %}</p>
                <p class="font-medium text-gray-900 dark:text-white">
                    {{ item.created_by.get_full_name|default:"-" }}
                </p>
            </div>
            <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">{% trans "Yaradılma Tarixi" %}</p>
                <p class="font-medium text-gray-900 dark:text-white">
                    {{ item.created_at|date:"d.m.Y H:i" }}
                </p>
            </div>
            <div>
                <p class="text-sm text-gray-500 dark:text-gray-400">{% trans "Son Yenilənmə" %}</p>
                <p class="font-medium text-gray-900 dark:text-white">
                    {{ item.updated_at|date:"d.m.Y H:i" }}
                </p>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 3. Form Səhifəsi (Create/Edit) Template

```html
{% extends 'base/base.html' %}
{% load static i18n %}

{% block title %}
    {% if form.instance.pk %}{% trans "Redaktə Et" %}{% else %}{% trans "Yeni Yarat" %}{% endif %} - Q360
{% endblock %}

{% block content %}
<div class="max-w-3xl mx-auto">
    <div class="flex items-center space-x-4 mb-6">
        <a href="{% url 'my_module:list' %}"
           class="p-2 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300
                  hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors">
            <i class="fas fa-arrow-left"></i>
        </a>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
            {% if form.instance.pk %}
                <i class="fas fa-edit text-amber-500 mr-2"></i>{% trans "Redaktə Et" %}
            {% else %}
                <i class="fas fa-plus-circle text-indigo-500 mr-2"></i>{% trans "Yeni Yarat" %}
            {% endif %}
        </h1>
    </div>

    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200
                dark:border-gray-700 p-6">
        <form method="post" enctype="multipart/form-data">
            {% csrf_token %}

            {% if form.errors %}
            <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800
                        rounded-lg p-4 mb-6">
                <div class="flex items-center">
                    <i class="fas fa-exclamation-circle text-red-500 mr-2"></i>
                    <p class="text-red-700 dark:text-red-400 font-medium">
                        {% trans "Xahiş edirik, aşağıdakı xətaları düzəldin." %}
                    </p>
                </div>
                <ul class="mt-2 text-sm text-red-600 dark:text-red-400 list-disc list-inside">
                    {% for field, errors in form.errors.items %}
                        {% for error in errors %}
                        <li>{{ error }}</li>
                        {% endfor %}
                    {% endfor %}
                </ul>
            </div>
            {% endif %}

            <div class="space-y-6">
                {% for field in form %}
                <div>
                    <label for="{{ field.id_for_label }}"
                           class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        {{ field.label }}
                        {% if field.field.required %}
                        <span class="text-red-500">*</span>
                        {% endif %}
                    </label>
                    {{ field }}
                    {% if field.help_text %}
                    <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">{{ field.help_text }}</p>
                    {% endif %}
                    {% if field.errors %}
                    <p class="mt-1 text-sm text-red-500">{{ field.errors.0 }}</p>
                    {% endif %}
                </div>
                {% endfor %}
            </div>

            <div class="flex items-center justify-end space-x-3 mt-8 pt-6 border-t
                        border-gray-200 dark:border-gray-700">
                <a href="{% url 'my_module:list' %}"
                   class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700
                          dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300
                          font-medium rounded-lg transition-colors">
                    {% trans "Ləğv Et" %}
                </a>
                <button type="submit"
                        class="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white
                               font-medium rounded-lg shadow-sm transition-colors">
                    <i class="fas fa-save mr-2"></i>
                    {% if form.instance.pk %}{% trans "Yadda Saxla" %}{% else %}{% trans "Yarat" %}{% endif %}
                </button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

---

## 4. Delete Confirmation Template

```html
{% extends 'base/base.html' %}
{% load i18n %}

{% block content %}
<div class="max-w-lg mx-auto mt-10">
    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200
                dark:border-gray-700 p-8 text-center">
        <div class="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center
                    justify-center mx-auto mb-4">
            <i class="fas fa-exclamation-triangle text-2xl text-red-500"></i>
        </div>
        <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
            {% trans "Silmək istədiyinizə əminsiniz?" %}
        </h2>
        <p class="text-gray-500 dark:text-gray-400 mb-6">
            <strong>"{{ item.title }}"</strong> {% trans "silinəcək. Bu əməliyyat geri qaytarıla bilməz." %}
        </p>
        <form method="post">
            {% csrf_token %}
            <div class="flex items-center justify-center space-x-3">
                <a href="{% url 'my_module:detail' item.pk %}"
                   class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700
                          dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300
                          font-medium rounded-lg transition-colors">
                    {% trans "Ləğv Et" %}
                </a>
                <button type="submit"
                        class="px-6 py-2 bg-red-600 hover:bg-red-700 text-white
                               font-medium rounded-lg transition-colors">
                    <i class="fas fa-trash mr-2"></i> {% trans "Sil" %}
                </button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
```

---

## 5. Sidebar-a Yeni Modul Əlavə Etmək

### Sidebar Link Pattern (templates/base/sidebar.html)

Sidebar-da hər bölmə accordion formatındadır. Yeni modul üçün uyğun accordion-un
`x-show` bölməsinə yeni `<a>` tag əlavə edilməlidir:

```html
<!-- Yeni link — mövcud accordion-un daxilinə əlavə et -->
<a href="{% url 'my_module:list' %}"
    class="flex items-center px-3 py-2 text-sm font-semibold rounded-lg transition-all
           duration-200 relative overflow-hidden group
           {% if '/my-module/' in request.path %}
               bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/30
               dark:to-blue-800/30 text-blue-700 dark:text-blue-400 border-l-4 border-blue-500
           {% else %}
               text-gray-900 font-bold dark:text-white hover:bg-gradient-to-r
               hover:from-gray-50 hover:to-gray-100 dark:hover:from-gray-700
               dark:hover:to-gray-600/50
           {% endif %}">
    <div class="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-indigo-500/10
                opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
    <i class="fas fa-icon-name w-6 text-center relative z-10 flex-shrink-0 text-lg
              transition-all" :class="sidebarOpen ? 'mr-3' : 'mx-auto text-xl'"></i>
    <span class="relative z-10 flex-1 whitespace-normal leading-tight"
          x-show="sidebarOpen">{% trans "Modul Adı" %}</span>
</a>
```

### RBAC-əsaslı Görünürlük

```html
{% if user.is_superuser %}
    <!-- Superuser-only linklər -->
{% endif %}

{% if user.is_admin or user.role == 'manager' %}
    <!-- Admin + Manager linklər -->
{% endif %}
```

---

## 6. Əlaqəli Fayllar Siyahısı (Hər Yeni Səhifə üçün)

```
apps/<module>/
├── models.py              ← Model (əgər yoxdursa)
├── forms.py               ← Django Form class
├── template_views.py      ← ListView, DetailView, CreateView, UpdateView, delete view
├── urls.py                ← URL patterns
├── serializers.py         ← DRF serializer (API lazımdırsa)
├── views.py               ← DRF ViewSet (API lazımdırsa)
├── admin.py               ← Admin qeydiyyatı
├── signals.py             ← Signal handlers (lazımdırsa)
└── tasks.py               ← Celery tasks (lazımdırsa)

templates/<module>/
├── list.html              ← Siyahı səhifəsi
├── detail.html            ← Detal səhifəsi
├── form.html              ← Create/Edit formu
├── confirm_delete.html    ← Silmə təsdiqi
└── (digər xüsusi səhifələr)

config/
├── urls.py                ← Root URL qeydiyyatı
├── api_urls.py            ← API router qeydiyyatı
└── settings.py            ← INSTALLED_APPS əlavəsi
```
