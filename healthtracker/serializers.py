from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from healthtracker.models import Activity


class ActivitySerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Activity
        #fields = '__all__'
        fields = ['id', 'name', 'activity_type', 'description', 'calories', 'duration', 'date_logged', 'user']


