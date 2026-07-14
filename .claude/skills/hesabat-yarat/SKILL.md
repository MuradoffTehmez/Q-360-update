---
name: hesabat-yarat
description: >
  Q360 layihəsində Django ilə hesabat, report generator və export xüsusiyyətlərini 
  yaratmaq üçün bələdçi. PDF, Excel (XLSX) və CSV formatlarında hesabatların asinxron
  generasiyası, weasyprint və openpyxl istifadəsini öyrədir. Tetikleyicilər: 
  "hesabat yarat", "report yaz", "pdf export", "excel export", "csv export", 
  "export funksiyası", "data export", "generate report", "report builder".
---

# Hesabat və Export Yaratma — Q360

Q360 layihəsində hesabatların və data exportlarının (PDF, Excel, CSV) yaradılması üçün standart pattern-lər aşağıdakı kimidir. Böyük hesabatlar üçün mütləq Celery istifadə olunmalıdır.

## 1. PDF Hesabatlar (WeasyPrint)

PDF hesabatlar HTML template-dən render olunur.

### Template (templates/reports/pdf/my_report.html)

```html
<!DOCTYPE html>
<html lang="az">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <style>
        @page {
            size: A4;
            margin: 2cm;
            @bottom-right {
                content: "Səhifə " counter(page) " / " counter(pages);
                font-size: 10pt;
                color: #666;
            }
        }
        body { font-family: 'Inter', sans-serif; font-size: 12pt; color: #333; }
        h1 { color: #1e3a8a; text-align: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 10px; }
        .metadata { margin-bottom: 30px; font-size: 10pt; color: #666; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f3f4f6; font-weight: bold; }
        .footer { margin-top: 50px; text-align: center; font-size: 9pt; color: #999; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    
    <div class="metadata">
        <p><strong>Yaradılma tarixi:</strong> {{ generated_at|date:"d.m.Y H:i" }}</p>
        <p><strong>Yaradan:</strong> {{ generated_by }}</p>
    </div>

    <table>
        <thead>
            <tr>
                <th>No</th>
                <th>Ad</th>
                <th>Status</th>
                <th>Tarix</th>
            </tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr>
                <td>{{ forloop.counter }}</td>
                <td>{{ item.title }}</td>
                <td>{{ item.get_status_display }}</td>
                <td>{{ item.created_at|date:"d.m.Y" }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div class="footer">
        <p>Q360 — Dövlət Sektoru üçün 360° Qiymətləndirmə Sistemi</p>
    </div>
</body>
</html>
```

### PDF Generator Sinfi

```python
# apps/reports/generators/pdf.py
from io import BytesIO
from django.template.loader import render_to_string
from django.utils import timezone
from weasyprint import HTML

class PDFGenerator:
    @staticmethod
    def generate(template_name, context, output_path=None):
        """
        HTML template-dən PDF yaradır.
        Əgər output_path verilirsə, fayla yazır, yoxsa BytesIO qaytarır.
        """
        # Standart context əlavələri
        context.update({
            'generated_at': timezone.now(),
        })
        
        # HTML render et
        html_string = render_to_string(f'reports/pdf/{template_name}.html', context)
        html = HTML(string=html_string)
        
        if output_path:
            html.write_pdf(output_path)
            return output_path
        else:
            pdf_file = html.write_pdf()
            return BytesIO(pdf_file)
```

## 2. Excel Hesabatlar (OpenPyxl)

```python
# apps/reports/generators/excel.py
from io import BytesIO
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

class ExcelGenerator:
    @staticmethod
    def generate(title, headers, data, output_path=None):
        """
        Verilmiş başlıqlar və data ilə Excel faylı yaradır.
        """
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Hesabat"
        
        # Stillər
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill("solid", fgColor="1E3A8A")
        header_align = Alignment(horizontal="center", vertical="center")
        border = Border(
            left=Side(style='thin'), right=Side(style='thin'),
            top=Side(style='thin'), bottom=Side(style='thin')
        )
        
        # Başlıq əlavə et (A1 hüceyrəsinə)
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(headers))
        title_cell = ws.cell(row=1, column=1, value=title)
        title_cell.font = Font(bold=True, size=14)
        title_cell.alignment = Alignment(horizontal="center")
        
        # Sütun başlıqları (Sətir 3)
        for col_num, header_title in enumerate(headers, 1):
            cell = ws.cell(row=3, column=col_num, value=header_title)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_align
            cell.border = border
            
            # Təxmini genişlik
            ws.column_dimensions[openpyxl.utils.get_column_letter(col_num)].width = max(len(header_title) + 5, 15)
            
        # Data doldur (Sətir 4-dən başlayaraq)
        for row_num, row_data in enumerate(data, 4):
            for col_num, cell_value in enumerate(row_data, 1):
                cell = ws.cell(row=row_num, column=col_num, value=cell_value)
                cell.border = border
                
        if output_path:
            wb.save(output_path)
            return output_path
        else:
            output = BytesIO()
            wb.save(output)
            output.seek(0)
            return output
```

## 3. Asinxron Hesabat İcraatı (View + Celery)

Böyük məlumatlar üçün hesabatlar birbaşa HTTP response-da qaytarılmır. Asinxron olaraq `Report` modelinə yazılır və istifadəçiyə bildiriş gedir.

### View Nümunəsi

```python
# apps/reports/views.py
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import View
from .tasks import generate_excel_report_task

class RequestReportView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        report_type = request.POST.get('report_type')
        filters = {
            'status': request.POST.get('status'),
            'date_from': request.POST.get('date_from'),
        }
        
        # Celery task-ı çağır
        generate_excel_report_task.delay(
            user_id=request.user.id,
            report_type=report_type,
            filters=filters
        )
        
        messages.success(request, "Hesabatın hazırlanması prosesi başladı. Bitdikdə bildiriş alacaqsınız.")
        return redirect(reverse('reports:list'))
```

### Celery Task Nümunəsi

```python
# apps/reports/tasks.py
from celery import shared_task
from django.core.files.base import ContentFile
from .models import GeneratedReport
from .generators.excel import ExcelGenerator
from apps.my_module.models import MyEntity

@shared_task(bind=True)
def generate_excel_report_task(self, user_id, report_type, filters):
    from apps.accounts.models import User
    user = User.objects.get(pk=user_id)
    
    # Yeni GeneratedReport obyekti yarat (status='processing')
    report = GeneratedReport.objects.create(
        title=f"Hesabat: {report_type}",
        requested_by=user,
        status='processing'
    )
    
    try:
        # Data topla
        queryset = MyEntity.objects.all()
        if filters.get('status'):
            queryset = queryset.filter(status=filters['status'])
            
        headers = ['No', 'Ad', 'Status', 'Tarix']
        data = []
        
        for i, item in enumerate(queryset, 1):
            data.append([
                i,
                item.title,
                item.get_status_display(),
                item.created_at.strftime('%d.%m.%Y %H:%M')
            ])
            
        # Excel yarat
        excel_io = ExcelGenerator.generate(
            title=f"Məlumat Hesabatı ({report_type})",
            headers=headers,
            data=data
        )
        
        # Report obyektinə faylı əlavə et
        file_name = f"report_{report_type}_{report.id}.xlsx"
        report.file.save(file_name, ContentFile(excel_io.read()))
        report.status = 'completed'
        report.save()
        
        # Bildiriş göndər
        from apps.notifications.services import notify_user
        notify_user(
            user=user,
            title="Hesabat hazırdır",
            message=f"'{report.title}' adlı hesabatınız hazırdır. Yükləyə bilərsiniz.",
            url=f"/reports/{report.id}/"
        )
        
    except Exception as e:
        report.status = 'failed'
        report.error_message = str(e)
        report.save()
        raise
```

## 4. Sinxron (Kiçik) Data Export (View)

Kiçik data setləri (məsələn, cari cədvəl səhifəsi) üçün sürətli CSV/Excel export birbaşa view-dan qaytarıla bilər.

```python
# Cədvəl görünüşündə (ListView) export funksiyası
import csv
from django.http import HttpResponse

class ExportCSVView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data_export.csv"'
        
        # UTF-8 BOM əlavə et ki, Excel-də Azərbaycan hərfləri düzgün görünsün
        response.write(u'\ufeff'.encode('utf8'))
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Ad', 'Status', 'Yaradan'])
        
        # Burada artıq Pagination olmamalıdır, bütün filter olunmuş queryset
        queryset = MyEntity.objects.select_related('created_by').all()
        
        for item in queryset:
            writer.writerow([
                item.id,
                item.title,
                item.get_status_display(),
                item.created_by.get_full_name()
            ])
            
        return response
```
