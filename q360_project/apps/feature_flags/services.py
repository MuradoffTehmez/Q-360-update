from django.core.cache import cache
from .models import FeatureFlag

class FeatureFlagManager:
    @staticmethod
    def is_active(flag_name, user=None):
        """
        Biznes məntiqi: Verilmiş flag-in statusunu öyrənmək. 
        Əgər redis cache-də varsa oradan oxuyur, yoxsa DB-dən.
        """
        cache_key = f"fflag_{flag_name}"
        cached_val = cache.get(cache_key)

        if cached_val is not None:
            active = cached_val
        else:
            flag = FeatureFlag.objects.filter(name=flag_name).first()
            if not flag:
                return False
            active = flag.is_active
            cache.set(cache_key, active, timeout=300)

        # Əgər globally aktivdirsə, rule-ları yoxla
        if not active:
            return False

        if user:
            flag = FeatureFlag.objects.filter(name=flag_name).first()
            # Məsələn: percentage rollout logic or specific user rule
            # Sadələşdirilmiş:
            for rule in flag.rules.all():
                if rule.target_users and user.id in rule.target_users:
                    return True
                if rule.target_departments and user.department_id in rule.target_departments:
                    return True
            
            # Xüsusi rule yoxdursa və is_active = True idisə:
            if not flag.rules.exists():
                 return True
                 
            return False

        return active
