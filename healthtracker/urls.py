
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from healthtracker.viewsets import ActivityViewSet
from healthtracker.views import LoginView

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activities')
urlpatterns = [
    path('', include(router.urls)),
    path('auth/login', LoginView.as_view(), name='login'),
]