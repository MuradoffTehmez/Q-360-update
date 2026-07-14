"""
Settings kateqoriya reyestri.
Hər kateqoriya: ad, ikon, təsvir və defolt parametrlər.
"""
from django.utils.translation import gettext_lazy as _

# slug -> {name, icon, description, defaults: [(key, default, type, desc)], stub}
CATEGORIES = {
    'general': {
        'name': _('Ümumi'), 'icon': 'fa-sliders',
        'description': _('Platformanın əsas parametrləri'),
        'defaults': [
            ('site_name', 'Q360', 'text', 'Sayt adı'),
            ('site_tagline', '360° Performance Suite', 'text', 'Şüar'),
            ('maintenance_mode', 'false', 'bool', 'Texniki xidmət rejimi'),
            ('items_per_page', '25', 'int', 'Siyahılarda səhifə ölçüsü'),
        ],
    },
    'localization': {
        'name': _('Lokalizasiya'), 'icon': 'fa-globe',
        'description': _('Dil, tarix və rəqəm formatları'),
        'defaults': [
            ('default_language', 'az', 'text', 'Defolt dil'),
            ('date_format', 'd.m.Y', 'text', 'Tarix formatı'),
            ('first_day_of_week', '1', 'int', 'Həftənin ilk günü (1=B.e)'),
        ],
    },
    'languages': {
        'name': _('Dillər'), 'icon': 'fa-language',
        'description': _('Aktiv interfeys dilləri'),
        'defaults': [
            ('enabled_languages', 'az,en', 'text', 'Aktiv dillər (vergüllə)'),
            ('allow_user_language', 'true', 'bool', 'İstifadəçi dil seçə bilər'),
        ],
    },
    'timezone': {
        'name': _('Saat qurşağı'), 'icon': 'fa-clock',
        'description': _('Vaxt zonası parametrləri'),
        'defaults': [
            ('default_timezone', 'Asia/Baku', 'text', 'Defolt saat qurşağı'),
            ('allow_user_timezone', 'false', 'bool', 'İstifadəçi saat qurşağı seçə bilər'),
        ],
    },
    'currency': {
        'name': _('Valyuta'), 'icon': 'fa-coins',
        'description': _('Valyuta və format parametrləri'),
        'defaults': [
            ('default_currency', 'AZN', 'text', 'Defolt valyuta'),
            ('currency_symbol', '₼', 'text', 'Valyuta simvolu'),
            ('decimal_places', '2', 'int', 'Onluq dəqiqlik'),
        ],
    },
    'branding': {
        'name': _('Brendinq'), 'icon': 'fa-palette',
        'description': _('Loqo, rənglər və görünüş'),
        'defaults': [
            ('primary_color', '#2563eb', 'text', 'Əsas rəng'),
            ('logo_url', '/static/images/favicon.svg', 'text', 'Loqo URL'),
            ('dark_mode_default', 'false', 'bool', 'Defolt qaranlıq rejim'),
        ],
    },
    'company': {
        'name': _('Şirkət'), 'icon': 'fa-building',
        'description': _('Təşkilat məlumatları'),
        'defaults': [
            ('company_name', '', 'text', 'Şirkət adı'),
            ('company_address', '', 'text', 'Ünvan'),
            ('company_phone', '', 'text', 'Telefon'),
            ('company_email', '', 'text', 'E-poçt'),
        ],
    },
    'security': {
        'name': _('Təhlükəsizlik'), 'icon': 'fa-shield-halved',
        'description': _('Sessiya və giriş təhlükəsizliyi'),
        'defaults': [
            ('session_timeout_minutes', '60', 'int', 'Sessiya vaxtı (dəq)'),
            ('max_login_attempts', '5', 'int', 'Maksimum giriş cəhdi'),
            ('lockout_minutes', '15', 'int', 'Bloklanma müddəti (dəq)'),
        ],
    },
    'authentication': {
        'name': _('Autentifikasiya'), 'icon': 'fa-key',
        'description': _('Giriş üsulları'),
        'defaults': [
            ('allow_registration', 'false', 'bool', 'Açıq qeydiyyat'),
            ('require_email_verification', 'true', 'bool', 'E-poçt təsdiqi tələb olunur'),
        ],
    },
    'password-policy': {
        'name': _('Şifrə siyasəti'), 'icon': 'fa-lock',
        'description': _('Şifrə tələbləri'),
        'defaults': [
            ('min_length', '12', 'int', 'Minimum uzunluq'),
            ('require_uppercase', 'true', 'bool', 'Böyük hərf tələbi'),
            ('require_digit', 'true', 'bool', 'Rəqəm tələbi'),
            ('require_symbol', 'true', 'bool', 'Simvol tələbi'),
            ('expiry_days', '90', 'int', 'Etibarlılıq müddəti (gün)'),
        ],
    },
    'mfa': {
        'name': _('MFA'), 'icon': 'fa-mobile-screen',
        'description': _('Çoxfaktorlu autentifikasiya'),
        'stub': True,
        'stub_text': _('MFA-nın mərkəzləşdirilmiş idarəetməsi real inteqrasiya spesifikasiyası tələb edir. '
                       'Hazırda istifadəçi səviyyəsində 2FA /accounts/2fa/setup/ vasitəsilə mövcuddur.'),
        'defaults': [],
    },
    'sso': {
        'name': _('SSO'), 'icon': 'fa-right-to-bracket',
        'description': _('Single Sign-On inteqrasiyası'),
        'stub': True,
        'stub_text': _('SAML/OIDC əsaslı SSO inteqrasiyası provayder seçimi və real spesifikasiya tələb edir.'),
        'defaults': [],
    },
    'integrations': {
        'name': _('İnteqrasiyalar'), 'icon': 'fa-plug',
        'description': _('Xarici sistem inteqrasiyaları'),
        'defaults': [
            ('slack_webhook_url', '', 'text', 'Slack webhook'),
            ('teams_webhook_url', '', 'text', 'MS Teams webhook'),
        ],
    },
    'api': {
        'name': _('API'), 'icon': 'fa-code',
        'description': _('API parametrləri'),
        'defaults': [
            ('api_enabled', 'true', 'bool', 'API aktiv'),
            ('rate_limit_per_minute', '300', 'int', 'Dəqiqəlik sorğu limiti'),
        ],
    },
    'api-keys': {
        'name': _('API Açarları'), 'icon': 'fa-key',
        'description': _('Xidmət API açarları'),
        'defaults': [
            ('internal_api_key', '', 'text', 'Daxili API açarı'),
        ],
        'sensitive': True,
    },
    'webhooks': {
        'name': _('Webhooks'), 'icon': 'fa-bolt',
        'description': _('Gedən webhook parametrləri'),
        'defaults': [
            ('webhook_timeout_seconds', '10', 'int', 'Timeout (san)'),
            ('webhook_retry_count', '3', 'int', 'Təkrar cəhd sayı'),
        ],
    },
    'email': {
        'name': _('E-poçt'), 'icon': 'fa-envelope',
        'description': _('SMTP və e-poçt parametrləri'),
        'defaults': [
            ('from_email', 'noreply@q360.az', 'text', 'Göndərən ünvan'),
            ('smtp_host', '', 'text', 'SMTP host'),
            ('smtp_port', '587', 'int', 'SMTP port'),
            ('smtp_use_tls', 'true', 'bool', 'TLS istifadə et'),
        ],
    },
    'sms': {
        'name': _('SMS'), 'icon': 'fa-comment-sms',
        'description': _('SMS provayder parametrləri'),
        'defaults': [
            ('sms_enabled', 'false', 'bool', 'SMS aktiv'),
            ('sms_sender_name', 'Q360', 'text', 'Göndərən adı'),
        ],
    },
    'storage': {
        'name': _('Yaddaş'), 'icon': 'fa-database',
        'description': _('Fayl saxlama parametrləri'),
        'defaults': [
            ('max_upload_mb', '25', 'int', 'Maksimum fayl ölçüsü (MB)'),
            ('allowed_extensions', 'pdf,docx,xlsx,png,jpg', 'text', 'İcazəli uzantılar'),
        ],
    },
    'backups': {
        'name': _('Rezerv nüsxələr'), 'icon': 'fa-box-archive',
        'description': _('Backup siyasəti'),
        'defaults': [
            ('backup_enabled', 'true', 'bool', 'Avtomatik backup'),
            ('backup_retention_days', '30', 'int', 'Saxlama müddəti (gün)'),
            ('backup_schedule_cron', '0 2 * * *', 'text', 'Cədvəl (cron)'),
        ],
    },
    'audit': {
        'name': _('Audit'), 'icon': 'fa-clipboard-list',
        'description': _('Audit jurnalı parametrləri'),
        'defaults': [
            ('audit_retention_days', '365', 'int', 'Jurnal saxlama müddəti (gün)'),
            ('log_read_actions', 'false', 'bool', 'Oxuma əməliyyatlarını da yaz'),
        ],
    },
    'licenses': {
        'name': _('Lisenziyalar'), 'icon': 'fa-certificate',
        'description': _('Lisenziya məlumatları'),
        'defaults': [
            ('license_key', '', 'text', 'Lisenziya açarı'),
            ('licensed_users', '100', 'int', 'Lisenziyalı istifadəçi sayı'),
        ],
        'sensitive': True,
    },
    'system': {
        'name': _('Sistem'), 'icon': 'fa-server',
        'description': _('Texniki sistem parametrləri'),
        'defaults': [
            ('debug_toolbar', 'false', 'bool', 'Debug paneli'),
            ('cache_ttl_seconds', '300', 'int', 'Keş TTL (san)'),
            ('celery_worker_count', '4', 'int', 'Celery işçi sayı'),
        ],
    },
}
