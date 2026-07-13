from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import (
    HealthCheckup, MentalHealthSurvey, FitnessProgram, MedicalClaim,
    WellnessChallenge, WellnessChallengeParticipation, HealthScore, StepTracking
)
from .serializers import (
    HealthCheckupSerializer, MentalHealthSurveySerializer, FitnessProgramSerializer,
    MedicalClaimSerializer, WellnessChallengeSerializer, WellnessChallengeParticipationSerializer,
    HealthScoreSerializer, StepTrackingSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class HealthCheckupViewSet(viewsets.ModelViewSet):
    queryset = HealthCheckup.objects.all().order_by('-scheduled_date')
    serializer_class = HealthCheckupSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'checkup_type', 'employee']
    search_fields = ['provider', 'location', 'notes']

class MentalHealthSurveyViewSet(viewsets.ModelViewSet):
    queryset = MentalHealthSurvey.objects.all().order_by('-survey_date')
    serializer_class = MentalHealthSurveySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee', 'stress_level', 'follow_up_required']

class FitnessProgramViewSet(viewsets.ModelViewSet):
    queryset = FitnessProgram.objects.all().order_by('-start_date')
    serializer_class = FitnessProgramSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'program_type']
    search_fields = ['title', 'description', 'location']

class MedicalClaimViewSet(viewsets.ModelViewSet):
    queryset = MedicalClaim.objects.all().order_by('-claim_date')
    serializer_class = MedicalClaimSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'claim_type', 'employee']
    search_fields = ['provider', 'description']

class WellnessChallengeViewSet(viewsets.ModelViewSet):
    queryset = WellnessChallenge.objects.all().order_by('-start_date')
    serializer_class = WellnessChallengeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'challenge_type']
    search_fields = ['title', 'description', 'goal']

class WellnessChallengeParticipationViewSet(viewsets.ModelViewSet):
    queryset = WellnessChallengeParticipation.objects.all()
    serializer_class = WellnessChallengeParticipationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['challenge', 'participant', 'completed']

class HealthScoreViewSet(viewsets.ModelViewSet):
    queryset = HealthScore.objects.all().order_by('-score_date')
    serializer_class = HealthScoreSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee']

class StepTrackingViewSet(viewsets.ModelViewSet):
    queryset = StepTracking.objects.all().order_by('-tracking_date')
    serializer_class = StepTrackingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee', 'tracking_date']
