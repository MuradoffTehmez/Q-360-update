from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ApprovalChain, ApprovalRequest, ApprovalDelegation
from .serializers import (
    ApprovalChainSerializer, ApprovalRequestSerializer, 
    ApprovalDelegationSerializer, ApprovalActionSerializer
)
from .services import ApprovalExecutionService

class ApprovalChainViewSet(viewsets.ModelViewSet):
    queryset = ApprovalChain.objects.all()
    serializer_class = ApprovalChainSerializer

class ApprovalDelegationViewSet(viewsets.ModelViewSet):
    queryset = ApprovalDelegation.objects.all()
    serializer_class = ApprovalDelegationSerializer

    def get_queryset(self):
        return self.queryset.filter(delegator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(delegator=self.request.user)

class PendingApprovalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User's pending approvals.
    """
    serializer_class = ApprovalRequestSerializer

    def get_queryset(self):
        # Mürəkkəb RBAC və Delegation yoxlanışları burada və ya filter backend-də olur
        return ApprovalRequest.objects.filter(status='PENDING')

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        approval_request = self.get_object()
        serializer = ApprovalActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        ApprovalExecutionService.process_approval(
            approval_request=approval_request,
            actor=request.user,
            action=serializer.validated_data['action'],
            comments=serializer.validated_data.get('comments', '')
        )
        return Response({"detail": "Approval processed successfully."})
