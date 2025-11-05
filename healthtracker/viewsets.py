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
        # Ensure status is set to 'planned' if not provided
        status = serializer.validated_data.get('status', 'planned')
        if status not in dict(Activity.STATUS_CHOICES).keys():
            status = 'planned'
        
        # Save with the user and validated status
        serializer.save(
            user=self.request.user,
            status=status
        )


