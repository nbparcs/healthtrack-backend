from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.admin import User
from rest_framework.serializers import ModelSerializer
from healthtracker.models import Activity


class ActivitySerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Activity
        fields = '__all__'
        #fields = ['id', 'name', 'activity_type', 'description', 'calories', 'duration', 'date_logged', 'user']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # confirm password

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn’t match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user