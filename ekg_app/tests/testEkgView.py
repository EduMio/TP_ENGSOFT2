from django.test import TestCase
from django.contrib.auth.models import User
from ekg_app.models import Patient, EKG
from django.urls import reverse

class EKGViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username="testuser", password="password")
        self.patient = Patient.objects.create(name="Test Patient", cpf="123.456.789-00", birth_date="1990-01-01", risk_level=2)
        self.ekg = EKG.objects.create(
            patient=self.patient,
            ekg_data="some_data",
            status=1,
            motive="Routine check",
            comorbidities="None",
            medications="None",
            symptoms="None",
            observations="None"
        )
        self.client.login(username="testuser", password="password")

    def test_ekg_list_view(self):
        response = self.client.get(reverse('admin:ekg_app_ekg_changelist'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Preferenciais")

    def test_ekg_dashboard_view(self):
        response = self.client.get(("/ekg_app/ekg/?patient__risk_level=2"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.patient.name)
