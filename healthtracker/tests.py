from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User

from healthtracker.models import Activity

# ---------------------------
# LOGIN API TESTS
# ---------------------------
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

# ---------------------------
# LOGOUT API TESTS
# ---------------------------
class LogoutAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_logout_success(self):
        login_response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpass'})
        token = login_response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_invalid(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# ---------------------------
# REGISTER API TESTS
# ---------------------------
class RegisterAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_register_success(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123'  # Password confirmation
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_missing_field(self):
        response = self.client.post(self.url, {
            'username': 'newuser',
            'email': 'test@example.com',
            'password': 'testpass123'
            # Missing password2
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# ACTIVITY API TESTS
# ---------------------------
class ActivityAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('activities-list')  # This is correct with the router

    # CREATE
    def test_create_activity(self):
        data = {
            'name': 'Morning Run',
            'activity_type': 'workout',
            'description': 'Ran 5km',
            'calories': 300,
            'duration': 30,
            'status': 'planned'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # READ (list)
    def test_list_activities(self):
        Activity.objects.create(user=self.user, name='Run', activity_type='workout')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # READ (detail)
    def test_activity_detail(self):
        activity = Activity.objects.create(
            user=self.user, 
            name='Run', 
            activity_type='workout',
            description='Test run',
            calories=100,
            duration=10
        )
        url = reverse('activities-detail', args=[activity.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the response data contains the activity details
        self.assertEqual(response.data['name'], 'Run')
        self.assertEqual(response.data['activity_type'], 'workout')
        self.assertEqual(response.data['description'], 'Test run')
        self.assertEqual(response.data['calories'], 100)
        self.assertEqual(response.data['duration'], 10)

    # UPDATE
    def test_update_activity(self):
        activity = Activity.objects.create(
            user=self.user, name='Yoga', activity_type='workout', duration=20, calories=150
        )
        url = reverse('activities-detail', args=[activity.id])
        response = self.client.put(url, {
            'name': 'Evening Yoga',
            'activity_type': 'workout',
            'duration': 45,
            'calories': 250
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # DELETE
    def test_delete_activity(self):
        activity = Activity.objects.create(
            user=self.user, name='Lunch', activity_type='meal', calories=600
        )
        url = reverse('activities-detail', args=[activity.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # UNAUTHORIZED CREATE
    def test_unauthorized_create(self):
        self.client.logout()
        data = {
            'name': 'Unauthorized Run',
            'activity_type': 'workout',
            'description': 'This should fail',
            'calories': 200,
            'duration': 20
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
