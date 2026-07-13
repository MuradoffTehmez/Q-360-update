from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ReportSchedule
from .serializers import ReportScheduleSerializer

class ReportScheduleViewSet(viewsets.ModelViewSet):
    queryset = ReportSchedule.objects.all()
    serializer_class = ReportScheduleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
