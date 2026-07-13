"""
Views for performance_reviews app.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import ReviewSession, ReviewNote, ReviewActionItem, CompetencyEvaluation
from .serializers import (
    ReviewSessionListSerializer, ReviewSessionDetailSerializer, ReviewSessionCreateSerializer,
    ReviewNoteSerializer, ReviewActionItemSerializer, CompetencyEvaluationSerializer
)


class ReviewSessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing 1-on-1 review sessions.
    Managers can create and manage sessions for their subordinates.
    Employees can view their own sessions.
    """
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status']
    ordering_fields = ['date']
    ordering = ['-date']

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return ReviewSession.objects.none()
        user = self.request.user
        if not user.is_authenticated:
            return ReviewSession.objects.none()
        # User can see sessions where they are manager or employee
        return ReviewSession.objects.filter(
            Q(manager=user) | Q(employee=user)
        ).select_related('manager', 'employee')

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewSessionCreateSerializer
        elif self.action == 'retrieve':
            return ReviewSessionDetailSerializer
        return ReviewSessionListSerializer

    def perform_create(self, serializer):
        # The user creating the session is the manager
        serializer.save(manager=self.request.user)

    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        session = self.get_object()
        if session.manager != request.user:
            return Response({"detail": "Yalnız rəhbər qeyd əlavə edə bilər."}, status=status.HTTP_403_FORBIDDEN)
            
        data = request.data.copy()
        data['session'] = session.id
        serializer = ReviewNoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save(session=session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_action_item(self, request, pk=None):
        session = self.get_object()
        if session.manager != request.user:
            return Response({"detail": "Yalnız rəhbər tapşırıq əlavə edə bilər."}, status=status.HTTP_403_FORBIDDEN)
            
        data = request.data.copy()
        data['session'] = session.id
        serializer = ReviewActionItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save(session=session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def evaluate_competency(self, request, pk=None):
        session = self.get_object()
        if session.manager != request.user:
            return Response({"detail": "Yalnız rəhbər qiymətləndirə bilər."}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = CompetencyEvaluationSerializer(data=request.data)
        if serializer.is_valid():
            # Check if evaluation already exists for this competency
            competency = serializer.validated_data.get('competency')
            existing = CompetencyEvaluation.objects.filter(session=session, competency=competency).first()
            if existing:
                # Update existing
                for attr, value in serializer.validated_data.items():
                    setattr(existing, attr, value)
                existing.save()
                return Response(CompetencyEvaluationSerializer(existing).data, status=status.HTTP_200_OK)
            else:
                serializer.save(session=session)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IsSessionManagerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.session.manager == request.user

    def has_permission(self, request, view):
        if request.method == 'POST':
            session_id = request.data.get('session')
            if session_id:
                try:
                    session = ReviewSession.objects.get(id=session_id)
                    return session.manager == request.user
                except ReviewSession.DoesNotExist:
                    pass
        return True

class ReviewNoteViewSet(viewsets.ModelViewSet):
    queryset = ReviewNote.objects.all()
    serializer_class = ReviewNoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsSessionManagerOrReadOnly]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ReviewNote.objects.none()
        user = self.request.user
        return ReviewNote.objects.filter(Q(session__manager=user) | Q(session__employee=user))

class ReviewActionItemViewSet(viewsets.ModelViewSet):
    queryset = ReviewActionItem.objects.all()
    serializer_class = ReviewActionItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsSessionManagerOrReadOnly]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ReviewActionItem.objects.none()
        user = self.request.user
        return ReviewActionItem.objects.filter(Q(session__manager=user) | Q(session__employee=user))

class CompetencyEvaluationViewSet(viewsets.ModelViewSet):
    queryset = CompetencyEvaluation.objects.all()
    serializer_class = CompetencyEvaluationSerializer
    permission_classes = [permissions.IsAuthenticated, IsSessionManagerOrReadOnly]
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CompetencyEvaluation.objects.none()
        user = self.request.user
        return CompetencyEvaluation.objects.filter(Q(session__manager=user) | Q(session__employee=user))
