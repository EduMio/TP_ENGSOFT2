from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
import time


class TestPatient(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.user = User.objects.create_superuser(
            username="tempuser", 
            password="tempPassword123", 
            email="tempuser@example.com"
        )
        
    def tearDown(self):
        self.browser.quit()

    def login(self):
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
        

    def test_patient_list_requires_login(self):
        self.browser.get(self.live_server_url+ '/ekg_app/patient/')
        WebDriverWait(self.browser, 10).until(
            EC.title_contains("Log in")
        )

        self.assertIn("Log in", self.browser.title)

        self.login()

        self.browser.get(self.live_server_url+'/ekg_app/patient/')
        time.sleep(2)
        self.assertIn("Select patient to change", self.browser.title)

    def test_add_patient_with_login(self):
        self.login()

        self.browser.get(self.live_server_url + "/ekg_app/patient/add/")

        name_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "name"))
        )

        name_field.send_keys("John Smith")
        self.browser.find_element(By.NAME, "cpf").send_keys("987.654.321-00")
        self.browser.find_element(By.NAME, "birth_date").send_keys("1990-05-15")
        self.browser.find_element(By.NAME, "risk_level").send_keys("2")

        self.browser.find_element(By.NAME, "_save").click()

        self.assertIn("/patient/", self.browser.current_url)
        table = self.browser.find_element(By.ID, "result_list")
        self.assertIn("John Smith", table.text)


    def test_invalid_cpf(self):
        self.login()

        self.browser.get(self.live_server_url + "/ekg_app/patient/add/")

        name_field = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.NAME, "name"))
        )
        name_field.send_keys('Gabriel Souza')

        cpf_input = self.browser.find_element(By.NAME, 'cpf')
        cpf_input.send_keys('1112223')  
        birth_date_input = self.browser.find_element(By.NAME, 'birth_date')
        birth_date_input.send_keys('1995-12-12')

        risk_level_select = self.browser.find_element(By.NAME, 'risk_level')
        risk_level_select.send_keys(Keys.ARROW_DOWN)

        self.browser.find_element(By.NAME, "_save").click()


        time.sleep(2)

        self.assertIn("CPF deve estar no formato", self.browser.page_source)