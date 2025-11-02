from django.urls import include, path
from rest_framework.routers import DefaultRouter

from healthtracker.viewsets import ActivityViewSet

router = DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activities')
urlpatterns = [
    path('', include(router.urls))
]