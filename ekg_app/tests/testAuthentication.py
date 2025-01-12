from django.test import TestCase
from django.contrib.auth.models import User

class AuthenticationTest(TestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_user_login(self):
        login = self.client.login(username="testuser", password="password")
        self.assertTrue(login)

    def test_user_logout(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

        # Log out the user
        self.client.logout()

        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Ensure the response is a redirect
        self.assertIn('/login/', response.url)  # Check that it redirects to the login page


    def test_invalid_login(self):
        login = self.client.login(username="invaliduser", password="password")
        self.assertFalse(login)