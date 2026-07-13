from .models import WorkflowInstance, WorkflowHistory, WorkflowInstanceStep
from apps.core.events import EventDispatcher

class WorkflowService:
    @staticmethod
    def start_workflow(template, requester, target_object):
        """
        Biznes məntiqi: Yeni Workflow Instance yaradılması və ilk addımın başladılması.
        """
        instance = WorkflowInstance.objects.create(
            template=template,
            requester=requester,
            content_object=target_object,
            status='IN_PROGRESS'
        )
        
        first_step = template.steps.first()
        if first_step:
            WorkflowInstanceStep.objects.create(
                instance=instance,
                step=first_step,
                status='PENDING'
                # assigned_to məntiqi Approval Engine və ya RBAC vasitəsilə təyin edilə bilər
            )
            
        WorkflowHistory.objects.create(
            instance=instance,
            actor=requester,
            action='STARTED'
        )
        
        EventDispatcher.publish('workflow.started', {'instance_id': instance.id})
        return instance

class TransitionService:
    @staticmethod
    def process_action(instance_step, actor, action, comments=''):
        """
        Biznes məntiqi: Addımın təsdiqlənməsi və ya rədd edilməsi və növbəti addıma keçid.
        """
        instance = instance_step.instance
        
        if action == 'APPROVE':
            instance_step.status = 'APPROVED'
            instance_step.save()
            
            WorkflowHistory.objects.create(
                instance=instance,
                step=instance_step.step,
                actor=actor,
                action='APPROVED',
                comments=comments
            )
            
            # Find next transition
            transition = instance_step.step.outgoing_transitions.first() # Sadələşdirilmiş
            if transition and transition.destination_step:
                WorkflowInstanceStep.objects.create(
                    instance=instance,
                    step=transition.destination_step,
                    status='PENDING'
                )
            else:
                instance.status = 'COMPLETED'
                instance.save()
                EventDispatcher.publish('workflow.completed', {'instance_id': instance.id})
                
        elif action == 'REJECT':
            instance_step.status = 'REJECTED'
            instance_step.save()
            
            instance.status = 'REJECTED'
            instance.save()
            
            WorkflowHistory.objects.create(
                instance=instance,
                step=instance_step.step,
                actor=actor,
                action='REJECTED',
                comments=comments
            )
            EventDispatcher.publish('workflow.rejected', {'instance_id': instance.id})
            
        return instance_step
