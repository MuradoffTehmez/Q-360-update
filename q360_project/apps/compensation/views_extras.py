from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from .models import PayGrade, SalaryBand, Currency, PayrollCycle

@login_required
def pay_grades_list(request):
    """Maaş dərəcələri."""
    grades = PayGrade.objects.all()
    return render(request, 'compensation/extras/pay_grades.html', {'title': _('Maaş Dərəcələri (Pay Grades)'), 'grades': grades})

@login_required
def salary_bands_list(request):
    """Maaş aralıqları."""
    bands = SalaryBand.objects.select_related('pay_grade', 'currency').all()
    return render(request, 'compensation/extras/salary_bands.html', {'title': _('Maaş Aralıqları (Salary Bands)'), 'bands': bands})

@login_required
def currencies_list(request):
    """Valyutalar."""
    currencies = Currency.objects.all()
    return render(request, 'compensation/extras/currencies.html', {'title': _('Valyutalar'), 'currencies': currencies})

@login_required
def payroll_cycles_list(request):
    """Ödəniş dövrləri."""
    cycles = PayrollCycle.objects.all()
    return render(request, 'compensation/extras/cycles.html', {'title': _('Ödəniş Dövrləri (Payroll Cycles)'), 'cycles': cycles})
