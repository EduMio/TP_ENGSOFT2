from django.test import TestCase
from django.contrib.auth.models import User
from .models import Patient

class PatientModelTest(TestCase):

    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username="testuser1", password="password")
        self.user2 = User.objects.create_user(username="testuser2", password="password")

        # Create test patients
        self.patient1 = Patient.objects.create(user=self.user1, age=30, risk_level=1)
        self.patient2 = Patient.objects.create(user=self.user2, age=45, risk_level=2)

    def test_patient_creation(self):
        self.assertEqual(Patient.objects.count(), 2)

    def test_patient_risk_level(self):
        self.assertEqual(self.patient1.risk_level, 1)
        self.assertEqual(self.patient2.risk_level, 2)

    def test_patient_age(self):
        self.assertEqual(self.patient1.age, 30)
        self.assertEqual(self.patient2.age, 45)

    def test_patient_user_link(self):
        self.assertEqual(self.patient1.user.username, "testuser1")
        self.assertEqual(self.patient2.user.username, "testuser2")

    def test_risk_ordering(self):
        patients = Patient.objects.all().order_by('risk_level')
        self.assertEqual(patients[0], self.patient1)
        self.assertEqual(patients[1], self.patient2)

class PatientViewTest(TestCase):

    def setUp(self):
        # Create users for patients
        self.user1 = User.objects.create_user(username="testuser1", password="password")
        self.user2 = User.objects.create_user(username="testuser2", password="password")

        # Create patients
        self.patient1 = Patient.objects.create(user=self.user1, age=30, risk_level=1)
        self.patient2 = Patient.objects.create(user=self.user2, age=45, risk_level=2)

        # Log in as one of the users
        self.client.login(username="testuser1", password="password")


    def test_dashboard_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ekg_app/dashboard.html')

    def test_dashboard_context(self):
        response = self.client.get('/')
        self.assertEqual(len(response.context['patients']), 2)

    def test_patient_risk_order_in_view(self):
        response = self.client.get('/')
        patients = response.context['patients']
        self.assertEqual(patients[0], self.patient1)
        self.assertEqual(patients[1], self.patient2)

class AdminTest(TestCase):

    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_superuser(username="admin", password="password")

    def test_admin_login(self):
        login = self.client.login(username="admin", password="password")
        self.assertTrue(login)

    def test_admin_access(self):
        self.client.login(username="admin", password="password")
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

class AuthenticationTest(TestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_user_login(self):
        login = self.client.login(username="testuser", password="password")
        self.assertTrue(login)

    def test_user_logout(self):
        # Log in and verify the user is logged in
        self.client.login(username="testuser", password="password")
        response = self.client.get('/')
        self.assertContains(response, "testuser")  # Ensure the username is present in the response

        # Log out the user
        self.client.logout()

        # Attempt to access the dashboard and verify the redirect
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # Ensure the response is a redirect
        self.assertIn('/accounts/login/', response.url)  # Check that it redirects to the login page


    def test_invalid_login(self):
        login = self.client.login(username="invaliduser", password="password")
        self.assertFalse(login)
