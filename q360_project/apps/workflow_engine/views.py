from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import WorkflowTemplate, WorkflowInstance, WorkflowInstanceStep
from .serializers import (
    WorkflowTemplateSerializer, WorkflowInstanceSerializer, 
    WorkflowInstanceStepSerializer, WorkflowActionSerializer
)
from .services import TransitionService

class WorkflowTemplateViewSet(viewsets.ModelViewSet):
    queryset = WorkflowTemplate.objects.all()
    serializer_class = WorkflowTemplateSerializer

class WorkflowInstanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WorkflowInstance.objects.all()
    serializer_class = WorkflowInstanceSerializer

class WorkflowTaskViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User's pending tasks.
    """
    serializer_class = WorkflowInstanceStepSerializer

    def get_queryset(self):
        return WorkflowInstanceStep.objects.filter(
            assigned_to=self.request.user, 
            status='PENDING'
        )

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        step = self.get_object()
        serializer = WorkflowActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        TransitionService.process_action(
            instance_step=step,
            actor=request.user,
            action=serializer.validated_data['action'],
            comments=serializer.validated_data.get('comments', '')
        )
        return Response({"detail": "Action processed successfully."})
