from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.reports.models import ReportBlueprint, ReportSchedule, ReportScheduleLog
from apps.accounts.models import User
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds the database with test report blueprints and schedules'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting report data seeding...')
        
        owner = User.objects.first()
        if not owner:
            self.stdout.write(self.style.ERROR('No users found in database. Cannot create blueprints.'))
            return

        # 1. Generate Blueprints
        blueprints_data = [
            {
                'title': 'Aylıq İşçi Performans İcmalı',
                'description': 'Bütün işçilərin aylıq performans göstəricilərinin detallı analizi.',
                'data_source': 'evaluations',
                'is_global': True,
                'columns': [
                    {'field': 'employee_name', 'label': 'İşçinin adı'},
                    {'field': 'department', 'label': 'Şöbə'},
                    {'field': 'total_score', 'label': 'Yekun Bal'},
                    {'field': 'evaluation_date', 'label': 'Qiymətləndirmə Tarixi'}
                ],
                'parameters': {'period': 'last_month'},
                'default_export_format': 'excel'
            },
            {
                'title': 'Şöbə üzrə Bacarıq Matrisi',
                'description': 'Müxtəlif şöbələrdəki əsas kompetensiyaların və bacarıq boşluqlarının vizualizasiyası.',
                'data_source': 'competencies',
                'is_global': True,
                'columns': [
                    {'field': 'department', 'label': 'Şöbə'},
                    {'field': 'competency', 'label': 'Kompetensiya'},
                    {'field': 'average_level', 'label': 'Orta Səviyyə'},
                    {'field': 'target_level', 'label': 'Hədəf Səviyyə'}
                ],
                'parameters': {'view': 'department_matrix'},
                'default_export_format': 'pdf'
            },
            {
                'title': 'Maaş Dəyişikliyi Proqnozu',
                'description': 'Növbəti rüb üçün performans əsaslı potensial maaş artımlarının simulyasiyası.',
                'data_source': 'evaluations',
                'is_global': False,
                'columns': [
                    {'field': 'employee_name', 'label': 'İşçinin adı'},
                    {'field': 'current_salary', 'label': 'Cari Maaş'},
                    {'field': 'proposed_increase', 'label': 'Təklif Edilən Artım'},
                    {'field': 'new_salary', 'label': 'Yeni Maaş'}
                ],
                'parameters': {'threshold': 85},
                'default_export_format': 'excel'
            },
            {
                'title': 'İşçi Dövriyyəsi Analizi',
                'description': 'Son bir ildə işdən çıxan və yeni işə qəbul olanların şöbələr üzrə statistikası.',
                'data_source': 'custom',
                'is_global': True,
                'columns': [
                    {'field': 'department', 'label': 'Şöbə'},
                    {'field': 'new_hires', 'label': 'Yeni Qəbul'},
                    {'field': 'departures', 'label': 'İşdən Çıxanlar'},
                    {'field': 'net_change', 'label': 'Xalis Dəyişiklik'}
                ],
                'parameters': {},
                'default_export_format': 'pdf'
            },
            {
                'title': 'Tibbi Sığorta Tələbləri',
                'description': 'Aktiv və gözləyən tibbi sığorta tələblərinin aylıq status hesabatı.',
                'data_source': 'custom',
                'is_global': False,
                'columns': [
                    {'field': 'employee_name', 'label': 'İşçinin adı'},
                    {'field': 'claim_date', 'label': 'Tarix'},
                    {'field': 'amount', 'label': 'Məbləğ'},
                    {'field': 'status', 'label': 'Status'}
                ],
                'parameters': {'status': 'pending'},
                'default_export_format': 'excel'
            },
        ]
        
        created_blueprints = []
        for i, data in enumerate(blueprints_data):
            slug = slugify(f"{data['title']}-{timezone.now().timestamp()}")
            blueprint, created = ReportBlueprint.objects.get_or_create(
                title=data['title'],
                defaults={
                    'slug': slug,
                    'description': data['description'],
                    'owner': owner,
                    'data_source': data['data_source'],
                    'is_global': data['is_global'],
                    'is_active': True,
                    'columns': data['columns'],
                    'configuration': data['parameters'],
                    'default_export_format': data['default_export_format']
                }
            )
            if not created:
                blueprint.description = data['description']
                blueprint.data_source = data['data_source']
                blueprint.columns = data['columns']
                blueprint.save()
            created_blueprints.append(blueprint)

        self.stdout.write(self.style.SUCCESS(f'Successfully created/updated {len(created_blueprints)} blueprints.'))

        # 2. Generate Schedules for the first 3 blueprints
        schedules_data = [
            {'frequency': 'daily', 'export_format': 'pdf'},
            {'frequency': 'weekly', 'export_format': 'excel'},
            {'frequency': 'monthly', 'export_format': 'pdf'},
        ]
        
        for i, schedule_info in enumerate(schedules_data):
            blueprint = created_blueprints[i]
            schedule, created = ReportSchedule.objects.get_or_create(
                blueprint=blueprint,
                created_by=owner,
                defaults={
                    'frequency': schedule_info['frequency'],
                    'export_format': schedule_info['export_format'],
                    'parameters': {},
                    'is_active': True,
                    'last_run': timezone.now() - timedelta(days=1),
                    'next_run': timezone.now() + timedelta(days=1),
                    'last_status': 'completed'
                }
            )
            schedule.recipients.add(owner)
            
            # Create a log entry for it
            ReportScheduleLog.objects.create(
                schedule=schedule,
                status='completed',
                message='Successfully generated and sent to recipients.',
                triggered_at=timezone.now() - timedelta(days=1),
                completed_at=timezone.now() - timedelta(hours=23, minutes=58)
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded ReportSchedules and logs.'))
