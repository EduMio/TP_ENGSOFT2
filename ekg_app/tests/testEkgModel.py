from django.test import TestCase
from django.contrib.auth.models import User
from ekg_app.models import Patient, MedicalReport, EKG

class EKGModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
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

    def test_ekg_creation(self):
        self.assertEqual(self.ekg.patient, self.patient)
        self.assertEqual(self.ekg.status, 1)
        self.assertEqual(self.ekg.motive, "Routine check")

    def test_ekg_status_update(self):
        report = MedicalReport.objects.create(
            ekg=self.ekg,
            heart_rate="Normal",
            p_wave="Normal",
            pr_interval="Normal",
            qrs_complex="Normal",
            qt_interval="Normal",
            conclusions="No issues",
        )
        
        self.ekg.refresh_from_db()
        
        self.assertEqual(self.ekg.status, 2)

    def test_ekg_str_method(self):
        expected_str = f"Paciente: {self.patient.name} - Grau de risco: {self.patient.risk_level} - Status: {self.ekg.status} - Motivo: Routine check"
        self.assertEqual(str(self.ekg), expected_str)