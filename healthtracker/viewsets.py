from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from healthtracker.models import Activity
from healthtracker.serializers import ActivitySerializer

class ActivityViewSet(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        activities = Activity.objects.filter(user=self.request.user)
        return activities

    #
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        serializer.save()
