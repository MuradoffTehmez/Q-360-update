from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

@shared_task
def send_async_password_reset_email(subject, email_template_name, user_pk, from_email, to_email, domain, site_name, use_https, extra_email_context=None):
    """Sends password reset email asynchronously."""
    from django.contrib.auth import get_user_model
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    
    User = get_user_model()
    print(f"Executing password reset for {user_pk} / {to_email}")
    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        return
        
    context = {
        'email': user.email,
        'domain': domain,
        'site_name': site_name,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': default_token_generator.make_token(user),
        'protocol': 'https' if use_https else 'http',
        **(extra_email_context or {}),
    }

    html_message = render_to_string(email_template_name, context)
    text_message = strip_tags(html_message)
    
    msg = EmailMultiAlternatives(subject, text_message, from_email, [to_email])
    msg.attach_alternative(html_message, "text/html")
    msg.send()

@shared_task
def import_users_task(file_path, uploader_id):
    """Imports users from a CSV/Excel file in the background."""
    import pandas as pd
    from django.contrib.auth import get_user_model
    import os
    import logging
    
    logger = logging.getLogger(__name__)
    User = get_user_model()
    
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        success_count = 0
        error_count = 0
        
        for index, row in df.iterrows():
            try:
                email = str(row.get('email', '')).strip()
                if not email or User.objects.filter(email=email).exists():
                    error_count += 1
                    continue
                
                # Validate email format
                from django.core.validators import validate_email
                from django.core.exceptions import ValidationError
                try:
                    validate_email(email)
                except ValidationError:
                    error_count += 1
                    continue
                    
                # Validate role
                role = str(row.get('role', '')).strip().lower()
                valid_roles = dict(User.ROLE_CHOICES).keys()
                if not role or role not in valid_roles:
                    error_count += 1
                    continue
                    
                username = str(row.get('username', email.split('@')[0])).strip()
                if User.objects.filter(username=username).exists():
                    username = f"{username}_{index}"
                    
                user = User(
                    username=username,
                    email=email,
                    first_name=str(row.get('first_name', '')).strip(),
                    last_name=str(row.get('last_name', '')).strip(),
                    role=role
                )
                user.set_password('Q360@Welcome2025!')  # Default password
                user.save()
                success_count += 1
            except Exception as e:
                logger.error(f"Error importing row {index}: {str(e)}")
                error_count += 1
                
        # Clean up file
        if os.path.exists(file_path):
            os.remove(file_path)
            
        logger.info(f"User import finished. Success: {success_count}, Errors: {error_count}")
        return {'success': success_count, 'errors': error_count}
        
    except Exception as e:
        logger.error(f"Fatal error in user import: {str(e)}")
        if os.path.exists(file_path):
            os.remove(file_path)
        return {'error': str(e)}
