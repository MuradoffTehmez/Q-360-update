import json
from .models import AbacPolicy

# Təsadüfi asılılıq əlavə etməmək üçün jsonlogic-python yerinə sadə təqlid (mock) evaluator.
# Əsl layihədə: from json_logic import jsonLogic
def simple_json_logic_eval(rule, data):
    # Sadələşdirilmiş nümunə (əsl jsonLogic bura qoşulacaq)
    return True

class AbacEvaluationService:
    @staticmethod
    def evaluate(user, resource, action, target_object=None):
        """
        Qayda mühərriki vasitəsilə ABAC icazəsini yoxlayır.
        """
        policies = AbacPolicy.objects.filter(
            resource=resource,
            action=action,
            is_deleted=False
        )

        if not policies.exists():
            # Əgər bu resource+action üçün heç bir ABAC qaydası yoxdursa
            # Default olaraq True (və ya layihənin tələbinə görə False) qaytarıla bilər.
            # Əgər qapalı sistemdirsə False, yoxsa True.
            return True

        # İstifadəçi və hədəf obyekt datalarını context olaraq yığırıq
        context = {
            "user": {
                "id": user.id,
                "department_id": user.department.id if hasattr(user, 'department') and user.department else None,
                # digər atributlar...
            },
            "resource": {
                "id": target_object.id if target_object else None,
                "owner_id": getattr(target_object, 'user_id', None) # nümunə
            }
        }

        # Ən azı bir policy icazə verirsə
        for policy in policies:
            if simple_json_logic_eval(policy.condition_json, context):
                return True
                
        return False
