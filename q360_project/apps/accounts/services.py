from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class AccountService:
    @staticmethod
    def change_user_password(user, new_password):
        """
        Biznes məntiqi: İstifadəçinin şifrəsinin dəyişdirilməsi.
        """
        user.set_password(new_password)
        user.save(update_fields=['password'])
        # Burada əlavə olaraq email göndərilməsi və ya event_bus trigger edilə bilər.
        return user

    @staticmethod
    def activate_user(user):
        """
        Biznes məntiqi: İstifadəçinin aktivləşdirilməsi.
        """
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=['is_active'])
        return user

    @staticmethod
    def deactivate_user(user):
        """
        Biznes məntiqi: İstifadəçinin deaktivləşdirilməsi.
        """
        if user.is_active:
            user.is_active = False
            user.save(update_fields=['is_active'])
        return user
