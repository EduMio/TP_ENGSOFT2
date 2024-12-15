from django.test import TestCase
from django.contrib.auth.models import User
from .models import Patient, MedicalReport, EKG
from django.urls import reverse


class PatientModelTest(TestCase):

    def setUp(self):
        # # Create test users
        # self.user1 = User.objects.create_user(username="testuser1", password="password")
        # self.user2 = User.objects.create_user(username="testuser2", password="password")

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

class PatientViewTest(TestCase):

    def setUp(self):
        # Create users for patients
        self.user1 = User.objects.create_superuser(username="testuser1", password="password")
        self.user2 = User.objects.create_superuser(username="testuser2", password="password")

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
  

class AdminTest(TestCase):

    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_superuser(username="admin", password="password")

    def test_admin_login(self):
        login = self.client.login(username="admin", password="password")
        self.assertTrue(login)

    def test_admin_access(self):
        self.client.login(username="admin", password="password")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

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
            conclusions="No issues detected"
        )
        self.ekg.refresh_from_db()
        self.assertEqual(self.ekg.status, 2)

    def test_ekg_str_method(self):
        expected_str = f"Paciente: {self.patient.name} - Grau de risco: {self.patient.risk_level} - Status: {self.ekg.status} - Motivo: Routine check"
        self.assertEqual(str(self.ekg), expected_str)

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
