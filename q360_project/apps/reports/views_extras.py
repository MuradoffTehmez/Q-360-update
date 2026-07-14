from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import CustomReport, ReportGenerationLog, SystemKPI

@login_required
def saved_reports(request):
    """
    Yadda saxlanılmış fərdi hesabatların siyahısı.
    """
    reports = CustomReport.objects.filter(owner=request.user, is_active=True).order_by('-created_at')
    context = {
        'title': _('Yadda Saxlanılmış Hesabatlar'),
        'reports': reports
    }
    return render(request, 'reports/saved_reports.html', context)


@login_required
def export_center(request):
    """
    Eksport mərkəzi (məlumatların kütləvi eksportu).
    """
    if request.method == 'POST':
        # Məlumatların eksportu prosesinə start vermək
        pass
        
    context = {
        'title': _('Eksport Mərkəzi')
    }
    return render(request, 'reports/export_center.html', context)


@login_required
def report_history(request):
    """
    Hesabat yaradılma tarixçəsi və eksport loqları.
    """
    logs = ReportGenerationLog.objects.filter(requested_by=request.user).order_by('-created_at')[:50]
    context = {
        'title': _('Hesabat Tarixçəsi'),
        'logs': logs
    }
    return render(request, 'reports/history.html', context)


@login_required
def data_warehouse(request):
    """
    Data Warehouse (KPI-lar və ümumi data bazası).
    """
    kpis = SystemKPI.objects.all().order_by('-date')[:30]
    context = {
        'title': _('Məlumat Anbarı (Data Warehouse)'),
        'kpis': kpis
    }
    return render(request, 'reports/data_warehouse.html', context)
