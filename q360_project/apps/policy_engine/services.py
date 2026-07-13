import json
from .models import Policy, PolicyVersion

# Yenə də sadə mock evaluator
def simple_json_logic_eval(rule, data):
    # Əslində bu hissədə JSONLogic python library istifadə olunacaq
    return True

class PolicyEvaluationService:
    @staticmethod
    def evaluate(policy_name, context_data):
        """
        Biznes məntiqi: Verilmiş siyasət adına uyğun ən son aktiv versiyanı tapıb JSONLogic ilə yoxlayır.
        """
        active_version = PolicyVersion.objects.filter(
            policy__name=policy_name,
            is_active=True
        ).first()

        if not active_version:
            # Əgər aktiv versiya yoxdursa, layihə tələbinə görə xəta verə və ya False qaytara bilər.
            return False

        return simple_json_logic_eval(active_version.rule_json, context_data)
