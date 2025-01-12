from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from ekg_app.models import Patient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from selenium.webdriver.support.ui import Select
import os

def create_fake_pdf(file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(100, 750, "Este é um arquivo de EKG falso.")
    c.drawString(100, 730, "O conteúdo deste arquivo não é real.")
    c.drawString(100, 710, "Você pode usá-lo para testar o upload de EKG.")
    c.showPage()
    c.save()

class TestEKGUploadAndReport(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.user = User.objects.create_superuser(
            username="tempuser", 
            password="tempPassword123", 
            email="tempuser@example.com"
        )
        self.patient1 = Patient.objects.create(name="patient1", cpf="537.214.789-03", birth_date="1994-01-01", risk_level=1)

        self.browser.get(self.live_server_url)
        
        username_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.send_keys("tempuser")

        password_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys("tempPassword123")
        
        password_field.send_keys(Keys.RETURN)

        WebDriverWait(self.browser, 10).until(
            EC.title_contains("ECG")
        )

        self.assertIn("ECG", self.browser.title)

        time.sleep(2)

    def test_incomplete_form_submission(self):
        
        self.browser.get(self.live_server_url+'/ekg_app/ekg/add')

        fake_pdf_path = os.path.abspath("fake_ekg_report.pdf")
        create_fake_pdf(fake_pdf_path)  

        patient_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "patient"))
        )

        patient_field.send_keys("patient1")
        self.browser.find_element(By.NAME, "ekg_data").send_keys(fake_pdf_path)
        # Não preencher o campo "motive"
        self.browser.find_element(By.NAME, "comorbidities").send_keys("Hipertensão")
        self.browser.find_element(By.NAME, "medications").send_keys("Losartana")
        self.browser.find_element(By.NAME, "symptoms").send_keys("Falta de ar")
        self.browser.find_element(By.NAME, "observations").send_keys("Observações adicionais")
        
        self.browser.find_element(By.NAME, "_save").click()

        time.sleep(2)

        self.assertIn("This field is required", self.browser.page_source)

        if os.path.exists(fake_pdf_path):
            os.remove(fake_pdf_path)

    def test_generate_medical_report(self):

        self.browser.get(self.live_server_url+'/ekg_app/ekg/add')

        fake_pdf_path = os.path.abspath("fake_ekg_report.pdf")
        create_fake_pdf(fake_pdf_path)  

        patient_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "patient"))
        )

        patient_field.send_keys("patient1")
        self.browser.find_element(By.NAME, "ekg_data").send_keys(fake_pdf_path)
        self.browser.find_element(By.NAME, "motive").send_keys("Dor no peito")
        self.browser.find_element(By.NAME, "comorbidities").send_keys("Hipertensão")
        self.browser.find_element(By.NAME, "medications").send_keys("Losartana")
        self.browser.find_element(By.NAME, "symptoms").send_keys("Falta de ar")
        self.browser.find_element(By.NAME, "observations").send_keys("Observações adicionais")
        
        self.browser.find_element(By.NAME, "_save").click()

        in_queue_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "status-container"))
        )

        time.sleep(2)

        self.assertIn("Na Fila: 1", in_queue_field.text)

        self.browser.get(self.live_server_url+'/ekg_app/medicalreport/add')

        select_element = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "ekg"))  
        )

        select = Select(select_element)

        select.select_by_index(1)
        self.browser.find_element(By.NAME, "heart_rate").send_keys("75 bpm")
        self.browser.find_element(By.NAME, "p_wave").send_keys("Normal")
        self.browser.find_element(By.NAME, "pr_interval").send_keys("200 ms")
        self.browser.find_element(By.NAME, "qrs_complex").send_keys("Normal")
        self.browser.find_element(By.NAME, "qt_interval").send_keys("400 ms")
        self.browser.find_element(By.NAME, "conclusions").send_keys("Resultado normal")
        
        self.browser.find_element(By.NAME, "_save").click()

        time.sleep(3)

        table = self.browser.find_element(By.ID, "result_list")
        self.assertIn("Report of patient1", table.text)

        if os.path.exists(fake_pdf_path):
            os.remove(fake_pdf_path)

    def tearDown(self):
        
        self.browser.quit()