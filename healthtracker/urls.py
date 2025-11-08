
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from healthtracker.viewsets import ActivityViewSet
from healthtracker.views import LoginView, LogoutView, RegisterView, mark_activity_completed

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activities')
urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('activities/<int:activity_id>/complete/', mark_activity_completed, name='mark_activity_completed'),


]