from django import forms
from django.utils.translation import gettext_lazy as _
from apps.reports.models import ReportSchedule, ReportBlueprint
from apps.accounts.models import User

class ReportScheduleForm(forms.ModelForm):
    """Form for creating and editing report schedules."""
    
    class Meta:
        model = ReportSchedule
        fields = [
            'blueprint',
            'frequency',
            'export_format',
            'recipients',
            'is_active',
        ]
        widgets = {
            'blueprint': forms.Select(attrs={'class': 'form-select'}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'export_format': forms.Select(attrs={'class': 'form-select'}),
            'recipients': forms.SelectMultiple(attrs={'class': 'form-select', 'data-choices': 'true'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['blueprint'].queryset = ReportBlueprint.objects.filter(is_active=True)
        self.fields['recipients'].queryset = User.objects.filter(is_active=True)
        self.fields['recipients'].help_text = _("Hesabatı alacaq istifadəçiləri seçin (çoxlu seçim mümkündür).")
