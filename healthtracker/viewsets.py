from rest_framework import viewsets, permissions
from healthtracker.models import Activity
from healthtracker.serializers import ActivitySerializer

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return activities belonging to the logged-in user
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set default status if not provided and assign the logged-in user
        if 'status' not in serializer.validated_data:
            serializer.validated_data['status'] = 'planned'
        serializer.save(user=self.request.user)


