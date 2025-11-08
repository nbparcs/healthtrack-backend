from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from healthtracker.models import Activity
from healthtracker.serializers import RegisterSerializer, ActivitySerializer


# Create your views here.
@api_view(['POST'])
def mark_activity_completed(request, activity_id):
    try:
        activity = Activity.objects.get(id=activity_id, user=request.user)
        activity.status = 'completed'
        activity.save()
        return Response({'message': 'Activity marked as completed successfully'})
    except Activity.DoesNotExist:
        return Response({'error': 'Activity not found'}, status=404)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]  #anyone can register
    serializer_class = RegisterSerializer

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=200)


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
