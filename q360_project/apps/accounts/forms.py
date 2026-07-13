"""
Forms for accounts app.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import User, Profile
from .security_utils import PasswordStrengthValidator, calculate_password_strength


class UserLoginForm(AuthenticationForm):
    """Custom login form."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'İstifadəçi adı və ya E-poçt',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Şifrə'
        })
    )


class UserRegistrationForm(UserCreationForm):
    """Form for user registration with extended fields."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-poçt ünvanı'
        })
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ad'
        })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Soyad'
        })
    )
    middle_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ata adı (opsional)'
        })
    )
    position = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Vəzifə'
        })
    )
    department = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+994XXXXXXXXX (opsional)'
        })
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Doğum tarixi (opsional)'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'middle_name', 'last_name',
                  'position', 'department', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set department queryset
        from apps.departments.models import Department
        self.fields['department'].queryset = Department.objects.filter(is_active=True).order_by('name')

        # Add custom styling to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Şifrə (ən az 8 simvol)'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Şifrəni təkrar daxil edin'
        })
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'İstifadəçi adı (unikal)'
        })

    def clean_email(self):
        """Validate email uniqueness."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Bu e-poçt ünvanı artıq istifadə olunur.')
        return email

    def clean_username(self):
        """Validate username uniqueness."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Bu istifadəçi adı artıq istifadə olunur.')
        return username

    def clean_password1(self):
        """Validate password strength."""
        password = self.cleaned_data.get('password1')
        if password:
            validator = PasswordStrengthValidator()
            validator.validate(password, self.instance)
        return password

    def save(self, commit=True):
        """Save user and create profile with date of birth."""
        user = super().save(commit=False)
        user.position = self.cleaned_data.get('position')
        user.department = self.cleaned_data.get('department')
        user.phone_number = self.cleaned_data.get('phone_number', '')

        if commit:
            user.save()

            # Create or update profile with date_of_birth
            profile, created = Profile.objects.get_or_create(user=user)
            date_of_birth = self.cleaned_data.get('date_of_birth')
            if date_of_birth:
                profile.date_of_birth = date_of_birth
                profile.save()

        return user


class UserUpdateForm(forms.ModelForm):
    """Form for updating user information."""

    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'email',
                  'phone_number', 'profile_picture', 'bio']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile."""

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'hire_date', 'education_level', 'specialization',
                  'work_email', 'work_phone', 'address', 'language_preference',
                  'email_notifications', 'sms_notifications']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'hire_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'education_level': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'work_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'work_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'language_preference': forms.Select(attrs={'class': 'form-select'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom password change form."""

    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Köhnə şifrə'
        })
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yeni şifrə',
            'id': 'id_new_password1'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yeni şifrə (təkrar)'
        })
    )

    def clean_new_password1(self):
        """Validate password strength."""
        password = self.cleaned_data.get('new_password1')
        if password:
            validator = PasswordStrengthValidator()
            validator.validate(password, self.user)
        return password

class AsyncPasswordResetForm(forms.Form):
    """Custom password reset form that uses Celery to send emails."""
    email = forms.EmailField(
        label="E-poçt",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'})
    )

    def save(self, domain_override=None, subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html', use_https=False,
             token_generator=None, from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        from django.contrib.sites.shortcuts import get_current_site
        from .tasks import send_async_password_reset_email
        from django.template import loader

        if not token_generator:
            token_generator = default_token_generator

        email = self.cleaned_data["email"]
        active_users = User.objects.filter(email__iexact=email, is_active=True)
        
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
            
        for user in active_users:
            if not user.has_usable_password():
                continue
                
            context = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            
            subject = loader.render_to_string(subject_template_name, context)
            subject = ''.join(subject.splitlines())
            
            send_async_password_reset_email.delay(
                subject=subject,
                email_template_name=email_template_name,
                user_pk=user.pk,
                from_email=from_email,
                to_email=user.email,
                domain=domain,
                site_name=site_name,
                use_https=use_https,
                extra_email_context=extra_email_context
            )
