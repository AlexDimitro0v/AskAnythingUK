from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
from selenium import webdriver
import unittest
import time


BASE_URL = "http://localhost:8000/"
DB_USER = User.objects.get(username="AlexD").userprofile


# Test and simulate the users' web browser interaction with our website
# To run the tests: python manage.py test users.tests.test_views
class TestViews(StaticLiveServerTestCase):

        def setUp(self):
            # Initiate ChromeDriver instance
            self.browser = webdriver.Chrome("chromedriver.exe")
            # Set default timeout for locating and element in the DOM (10 seconds)
            self.browser.implicitly_wait(10)
            # Maximize window
            self.browser.maximize_window()
            # Open the AskAnything login page
            self.browser.get(BASE_URL + "login/")
            # Log in the user
            self.browser.find_element_by_id('id_username').send_keys("AlexD")
            self.browser.find_element_by_id('id_password').send_keys("testing555")
            self.browser.find_element_by_id('login_button').click()
            # Get the user object
            self.user = DB_USER

        def verify_url(self, actual_url, expected_url):
            """ Compare 2 arguments """
            unittest.TestCase.assertEquals(self, actual_url, expected_url,
                                           "Actual BASE_URL: " + actual_url + " is not equal to expected BASE_URL: " + expected_url)

        def test_get_premium_feature(self):
            # Try to access the get-premium page
            self.browser.get(BASE_URL + "get-premium/")

            if self.user.premium:
                actual_url = self.browser.current_url
                # If the user is already premium, he must be redirected to the dashboard
                self.verify_url(actual_url=actual_url, expected_url=BASE_URL + "dashboard/")
            else:
                actual_url = self.browser.current_url
                # If the user is not premium continue as normal
                self.verify_url(actual_url=actual_url, expected_url=BASE_URL+"get-premium/")

            if BASE_URL + "dashboard/" == self.browser.current_url:
                # That would mean the user has already become premium; if so:
                self.browser.get(BASE_URL + "settings/?tab=subscription")
                self.browser.find_element_by_id("cancel-subscription").click()
                self.browser.find_element_by_id("yes").click()

                # Test that the user is able to cancel the subscription and resubscribe again by clicking on
                # the "More Information", i.e. subscribe button
                self.assertTrue("More Information" in self.browser.page_source)
                self.browser.find_element_by_name("subscription").click()

            self.browser.find_element_by_id("try-premium").click()
            self.browser.find_element_by_id("yes").click()

            # The user has a payment method:
            if self.user.payment_method:
                actual_url = self.browser.current_url
                # The user must see information about the subscription and be redirected to the subscription
                # information page
                self.verify_url(actual_url=actual_url, expected_url=BASE_URL + "settings/?tab=subscription")
                self.assertTrue("You are currently on a premium plan" in self.browser.page_source)

            # The user doesn't have a payment method:
            else:
                actual_url = self.browser.current_url
                # The user must be redirected to the billing page in order to provide a payment method
                self.verify_url(actual_url=actual_url,
                                expected_url=BASE_URL + "settings/?tab=billing&next=/get-premium/")

        def tearDown(self):
            self.browser.close()
