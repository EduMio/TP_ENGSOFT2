from django.test import TestCase
from django.contrib.auth.models import User
from ekg_app.models import Patient

class PatientViewTest(TestCase):

    def setUp(self):
        # Create users for patients
        self.user1 = User.objects.create_superuser(username="testuser1", password="password")

        # Create patients
        self.patient1 = Patient.objects.create(name="patient1", cpf="537.214.789-03", birth_date="1994-01-01", risk_level=1)
        self.patient2 = Patient.objects.create(name="patient2", cpf="645.928.347-10", birth_date="1979-04-15", risk_level=2)

        # Log in as one of the users
        self.client.login(username="testuser1", password="password")

    def test_patient_list_view(self):
        response = self.client.get('/ekg_app/patient/')
        
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.patient1.name)
        self.assertContains(response, self.patient2.name)

    def test_patient_delete_view(self):
    
        response = self.client.get(f'/ekg_app/patient/{self.patient1.id_patient}/delete/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Are you sure you want to delete")

        response = self.client.post(f'/ekg_app/patient/{self.patient1.id_patient}/delete/', data={'post': 'yes'}, follow=True)

        self.assertRedirects(response, '/ekg_app/patient/')

        self.assertFalse(Patient.objects.filter(id_patient=self.patient1.id_patient).exists())

    def test_patient_edit_view(self):
        response = self.client.get(f'/ekg_app/patient/{self.patient1.id_patient}/change/', follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Change patient")

        response = self.client.post(f'/ekg_app/patient/{self.patient1.id_patient}/change/', {
            'name': 'updated_patient',
            'cpf': '537.214.789-03',
            'birth_date': '1994-01-01',
            'risk_level': 2,
        }, follow=True)

        self.assertContains(response, "updated_patient")
        self.assertNotContains(response, "patient1")

    def test_patient_create_view(self):
        response = self.client.get('/ekg_app/patient/add/', follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add patient")

        response = self.client.post('/ekg_app/patient/add/', {
            'name': 'new_patient',
            'cpf': '123.456.789-00',
            'birth_date': '1990-05-22',
            'risk_level': 3,
        }, follow=True)

        self.assertContains(response, "new_patient")