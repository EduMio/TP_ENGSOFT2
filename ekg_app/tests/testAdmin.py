from django.test import TestCase
from django.contrib.auth.models import User

class AdminTest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(username="admin", password="password")

    def test_admin_login(self):
        login = self.client.login(username="admin", password="password")
        self.assertTrue(login)

    def test_admin_access(self):     
        self.client.login(username="admin", password="password")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)