from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User

from healthtracker.models import Activity


# Create your tests here.

class LoginAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.url = reverse('login')

    def test_login_success(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)


class LogoutAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_logout_success(self):
        # Login to get token
        login_response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass'})
        token = login_response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Logout with token
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_invalid(self):
        # No token — unauthorized
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ActivityAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.url = reverse('activity-list')

    def test_create_activity(self):
        data = {
            'name': 'Morning Run',
            'activity_type': 'workout',
            'description': 'Ran 5km around the park',
            'calories': 300,
            'duration': 30
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_activity(self):
        activity = Activity.objects.create(
            user=self.user, name='Yoga', activity_type='workout', duration=20, calories=150
        )
        url = reverse('activity-detail', args=[activity.id])
        response = self.client.put(url, {
            'name': 'Evening Yoga',
            'activity_type': 'workout',
            'duration': 45,
            'calories': 250
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_activity(self):
        activity = Activity.objects.create(
            user=self.user, name='Lunch', activity_type='meal', calories=600
        )
        url = reverse('activity-detail', args=[activity.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
