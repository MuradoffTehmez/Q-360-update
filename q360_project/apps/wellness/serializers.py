from rest_framework import serializers
from .models import (
    HealthCheckup, MentalHealthSurvey, FitnessProgram, MedicalClaim,
    WellnessChallenge, WellnessChallengeParticipation, HealthScore, StepTracking
)

class HealthCheckupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCheckup
        fields = '__all__'

class MentalHealthSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = MentalHealthSurvey
        fields = '__all__'

class FitnessProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessProgram
        fields = '__all__'

class MedicalClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalClaim
        fields = '__all__'

class WellnessChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessChallenge
        fields = '__all__'

class WellnessChallengeParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessChallengeParticipation
        fields = '__all__'

class HealthScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthScore
        fields = '__all__'

class StepTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepTracking
        fields = '__all__'
