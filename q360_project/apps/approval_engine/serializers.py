from rest_framework import serializers
from .models import ApprovalChain, ApprovalRequest, ApprovalLog, ApprovalDelegation

class ApprovalChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalChain
        fields = '__all__'

class ApprovalRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRequest
        fields = '__all__'

class ApprovalDelegationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalDelegation
        fields = '__all__'

class ApprovalActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['APPROVE', 'REJECT'])
    comments = serializers.CharField(required=False, allow_blank=True)
