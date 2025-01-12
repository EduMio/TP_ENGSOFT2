from django.test import TestCase
from django.contrib.auth.models import User
from ekg_app.models import Patient, MedicalReport, EKG

class MedicalReportModelTest(TestCase):

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

    def test_medical_report_creation(self):
        report = MedicalReport.objects.create(
            ekg=self.ekg,
            heart_rate="Normal",
            p_wave="Normal",
            pr_interval="Normal",
            qrs_complex="Normal",
            qt_interval="Normal",
            conclusions="No issues detected"
        )
        self.assertEqual(report.ekg, self.ekg)
        self.assertEqual(report.conclusions, "No issues detected")

    def test_medical_report_status_update(self):
        report = MedicalReport.objects.create(
            ekg=self.ekg,
            heart_rate="Normal",
            p_wave="Normal",
            pr_interval="Normal",
            qrs_complex="Normal",
            qt_interval="Normal",
            conclusions="No issues detected"
        )
        self.ekg.refresh_from_db()
        self.assertEqual(self.ekg.status, 2)

    def test_medical_report_str_method(self):
        report = MedicalReport.objects.create(
            ekg=self.ekg,
            heart_rate="Normal",
            p_wave="Normal",
            pr_interval="Normal",
            qrs_complex="Normal",
            qt_interval="Normal",
            conclusions="No issues detected"
        )
        expected_str = (f"Report of {self.ekg.patient.name} - Heart Rate: Normal, "
                        f"P Wave: Normal, PR Interval: Normal, "
                        f"QRS Complex: Normal, QT Interval: Normal")
        self.assertEqual(str(report), expected_str)
