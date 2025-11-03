from rest_framework import viewsets, permissions
from healthtracker.models import Activity
from healthtracker.serializers import ActivitySerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            return Activity.objects.filter(user=self.request.user)
        return Activity.objects.all()

    def perform_create(self, serializer):
        # Save activity with user if authenticated, otherwise save without user
        if hasattr(self.request, 'user') and self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()  # This will save with user=Noness


