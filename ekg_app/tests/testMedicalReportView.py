from django.test import TestCase
from django.contrib.auth.models import User
from ekg_app.models import Patient, MedicalReport, EKG
from django.urls import reverse

class MedicalReportViewTest(TestCase):

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
        self.medical_report = MedicalReport.objects.create(
            ekg=self.ekg,
            heart_rate="Normal",
            p_wave="Normal",
            pr_interval="Normal",
            qrs_complex="Normal",
            qt_interval="Normal",
            conclusions="No issues detected"
        )
        self.client.login(username="testuser", password="password")

    def test_medical_report_list_view(self):
        response = self.client.get(reverse('admin:ekg_app_medicalreport_changelist'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.patient.name)

    def test_medical_report_detail_view(self):
        response = self.client.get(reverse('admin:ekg_app_medicalreport_change', args=[self.medical_report.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.patient.name)
        self.assertContains(response, self.medical_report.heart_rate)
        self.assertContains(response, self.medical_report.conclusions)
        self.assertContains(response, "Normal")

    def test_medical_report_creation(self):
        response = self.client.post(reverse('admin:ekg_app_medicalreport_add'), {
            'ekg': self.ekg.id_ekg,
            'heart_rate': "Normal",
            'p_wave': "Normal",
            'pr_interval': "Normal",
            'qrs_complex': "Normal",
            'qt_interval': "Normal",
            'conclusions': "No issues detected"
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MedicalReport.objects.count(), 2)
