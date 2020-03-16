from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from main.models import Area
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import unittest
import time

def create_user():
    user = User.objects.create(username='testuser',is_active=True,email="test@test.com")
    user.set_password('12345')
    user.save()

    # Add the following pre-defined categories:
    area_names = ["Video & Animation", "Graphics & Design", "Writing", "Translation", "Technology", "Music & Audio"]
    for name in area_names:
        if not Area.objects.filter(name=name).exists():
            area = Area(name=name)
            area.save()

def login_user(test):
    test.client = Client()
    test.client.login(username='testuser', password='12345')


# Test all pages functional for logged-in users
class LoggedIn(TestCase):
    def setUp(self):
        create_user()
        login_user(self)

    def test_logged_in_pages(self):
        # All of these should be accessible
        pages_to_test = ['profile-page','settings-page','dashboard','archive','new-feedback-request-page','get-premium-page']
        for page in pages_to_test:
            response = self.client.get(reverse(page))
            self.assertEqual(response.status_code, 200)

    def test_feedback_requests(self):
        response = self.client.get(reverse('feedback-requests-page'))
        self.assertRedirects(response, "/", status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        for i in range(1,7):
            response = self.client.get(reverse('feedback-requests-page')+"?area-filter="+str(i))
            self.assertEqual(response.status_code, 200)

        # Non-existent areas result in redirect
        for i in [0,8]:
            response = self.client.get(reverse('feedback-requests-page')+"?area-filter="+str(i))
            self.assertRedirects(response, "/", status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_search(self):
        response = self.client.get(reverse('search-page'))
        self.assertRedirects(response, "/", status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        response = self.client.get(reverse('search-page')+"?q=Test")
        self.assertEqual(response.status_code, 200)


    def test_logout(self):
        response = self.client.get(reverse('logout-page'))
        self.assertRedirects(response, reverse('landing-page'), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

        # Now pages should not be accessible
        pages_to_test = ['profile-page','settings-page','dashboard','archive','new-feedback-request-page','get-premium-page']
        for page in pages_to_test:
            response = self.client.get(reverse(page))
            self.assertRedirects(response, "/login/?next="+reverse(page), status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_premium(self):
        response = self.client.get(reverse("get-premium-page"))
        self.assertEqual(response.status_code, 200)


class SubmittingForms(unittest.TestCase):
    def setUp(self):
        login_user(self)
        self.driver = webdriver.Chrome()

    def test_registration(self):
        self.driver.get("http://localhost:8000/register/")

        # Failed register
        self.driver.find_element_by_id('register_button').click()
        self.assertIn("http://localhost:8000/register/", self.driver.current_url)
        self.driver.get("http://localhost:8000/register/")

        # Failed register
        self.driver.find_element_by_id('id_first_name').send_keys("First")
        self.driver.find_element_by_id('id_last_name').send_keys("Last")
        self.driver.find_element_by_id('id_username').send_keys("TestName")
        self.driver.find_element_by_id('id_email').send_keys("test@testtest.com")
        self.driver.find_element_by_id('id_password1').send_keys("passwordtestpassword")
        self.driver.find_element_by_id('id_password2').send_keys("differenttestpassword")

        self.driver.find_element_by_id('register_button').click()
        self.assertIn("http://localhost:8000/register/", self.driver.current_url)
        self.driver.get("http://localhost:8000/register/")

        # Successful register
        self.driver.find_element_by_id('id_first_name').send_keys("First")
        self.driver.find_element_by_id('id_last_name').send_keys("Last")
        self.driver.find_element_by_id('id_username').send_keys("TestName")
        self.driver.find_element_by_id('id_email').send_keys("test@testtest.com")
        self.driver.find_element_by_id('id_password1').send_keys("passwordtestpassword")
        self.driver.find_element_by_id('id_password2').send_keys("passwordtestpassword")

        self.driver.find_element_by_id('register_button').click()
        self.assertIn("http://localhost:8000/landing-page/", self.driver.current_url)

    def test_login(self):
        self.driver.get("http://localhost:8000/login/")

        # Failed login
        self.driver.find_element_by_id('id_username').send_keys("lukas")
        self.driver.find_element_by_id('id_password').send_keys("afsrgthrgsefseguisnos")
        self.driver.find_element_by_id('login_button').click()
        self.assertIn("http://localhost:8000/login/", self.driver.current_url)

        # Successful login
        self.driver.find_element_by_id('id_username').send_keys("lukas")
        self.driver.find_element_by_id('id_password').send_keys("lukasadomaitis")
        self.driver.find_element_by_id('login_button').click()
        self.assertIn("http://localhost:8000/", self.driver.current_url)

    def test_new_feedback_request(self):
        self.driver.get("http://localhost:8000/login/")
        if "http://localhost:8000/login/" == self.driver.current_url:
            self.driver.find_element_by_id('id_username').send_keys("lukas")
            self.driver.find_element_by_id('id_password').send_keys("lukasadomaitis")
            self.driver.find_element_by_id('login_button').click()

        self.driver.get("http://localhost:8000/new-feedback-request/")

        # Unsuccessful new feedback request
        self.driver.find_element_by_id('submit_button').click()
        self.assertIn("http://localhost:8000/new-feedback-request/", self.driver.current_url)

        self.driver.get("http://localhost:8000/new-feedback-request/")

        # Unsuccessful new feedback request
        self.driver.find_element_by_id('title').send_keys("First")
        self.driver.find_element_by_id('description').send_keys("Last")
        self.driver.find_element_by_id('reward').send_keys("-10")
        self.driver.find_element_by_id('limit').send_keys("-10")
        self.driver.find_element_by_id('file-upload').send_keys("C:\\___\\logo.png")
        self.driver.find_element_by_id('submit_button').click()
        self.assertIn("http://localhost:8000/new-feedback-request/", self.driver.current_url)

        self.driver.get("http://localhost:8000/new-feedback-request/")

        # Successful new feedback request
        self.driver.find_element_by_id('title').send_keys("First")
        self.driver.find_element_by_id('description').send_keys("Last")
        self.driver.find_element_by_id('reward').send_keys("10")
        self.driver.find_element_by_id('limit').send_keys("10")
        self.driver.find_element_by_id('file-upload').send_keys("C:\\___\\logo.png")

        self.driver.find_element_by_id('submit_button').click()
        time.sleep(5)
        self.assertIn("http://localhost:8000/dashboard/", self.driver.current_url)


    def tearDown(self):
        self.driver.quit
