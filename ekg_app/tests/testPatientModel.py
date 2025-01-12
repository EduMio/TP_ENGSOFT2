from django.test import TestCase
from django.contrib.auth.models import User
from ekg_app.models import Patient

class PatientModelTest(TestCase):

    def setUp(self):
        # Create test patients
        self.patient1 = Patient.objects.create(name="patient1", cpf="537.214.789-03", birth_date="1994-01-01", risk_level=1)
        self.patient2 = Patient.objects.create(name="patient2", cpf="645.928.347-10", birth_date="1979-04-15", risk_level=2)

    def test_patient_creation(self):
        self.assertEqual(Patient.objects.count(), 2)

    def test_patient_risk_level(self):
        self.assertEqual(self.patient1.risk_level, 1)
        self.assertEqual(self.patient2.risk_level, 2)

    def test_patient_age(self):
        self.assertEqual(self.patient1.birth_date, "1994-01-01")
        self.assertEqual(self.patient2.birth_date, "1979-04-15")

    def test_patient_user_link(self):
        self.assertEqual(self.patient1.name, "patient1")
        self.assertEqual(self.patient2.name, "patient2")

    def test_risk_ordering(self):
        patients = Patient.objects.all().order_by('risk_level')
        self.assertEqual(patients[0], self.patient1)
        self.assertEqual(patients[1], self.patient2)
