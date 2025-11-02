from rest_framework import viewsets
from healthtracker.models import Activity
from healthtracker.serializers import ActivitySerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        # Return all activities (no authentication filtering)
        return Activity.objects.all()

    def perform_create(self, serializer):
        # Save activity without linking to a user
        serializer.save()
