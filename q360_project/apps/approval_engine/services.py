from django.utils import timezone
from .models import ApprovalRequest, ApprovalLog, ApprovalDelegation
from apps.core.events import EventDispatcher

class DelegationService:
    @staticmethod
    def get_actual_approver(user):
        """
        Biznes məntiqi: Əgər istifadəçi məzuniyyətdədirsə və ya delegasiya edibsə,
        aktiv delegasiyanı tapıb əvəzedicini qaytarır.
        """
        now = timezone.now()
        delegation = ApprovalDelegation.objects.filter(
            delegator=user,
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).first()
        
        if delegation:
            return delegation.delegatee
        return user

class ApprovalExecutionService:
    @staticmethod
    def process_approval(approval_request, actor, action, comments=''):
        """
        Biznes məntiqi: Təsdiq və ya Rədd qərarının işlənməsi.
        """
        actual_actor = DelegationService.get_actual_approver(actor)
        # Reallıqda actual_actor-un current_node üçün yetkili olub-olmaması da yoxlanılmalıdır.

        ApprovalLog.objects.create(
            request=approval_request,
            node=approval_request.current_node,
            actor=actual_actor,
            action=action,
            comments=comments
        )

        if action == 'APPROVE':
            # Növbəti node-u tap
            next_node = approval_request.chain.nodes.filter(
                order__gt=approval_request.current_node.order
            ).first()

            if next_node:
                approval_request.current_node = next_node
                approval_request.save()
            else:
                approval_request.status = 'APPROVED'
                approval_request.current_node = None
                approval_request.save()
                EventDispatcher.publish('approval.completed', {'request_id': approval_request.id})

        elif action == 'REJECT':
            approval_request.status = 'REJECTED'
            approval_request.current_node = None
            approval_request.save()
            EventDispatcher.publish('approval.rejected', {'request_id': approval_request.id})

        return approval_request
