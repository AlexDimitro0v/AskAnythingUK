from django.test import TestCase
from users.forms import UserRegistrationForm, PublicInformationForm, PrivateInformationForm


class Forms(TestCase):
    def test_registration_form(self):
        # 1 Successful
        form_data = {"first_name": "John", "last_name": "Doe", "username": "johndoe", "email": "repeat@gmail.com",
                     "password1": "test12345", "password2": "test12345"}
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

        # 1 Unsuccessful - user trying to enter passwords that do not match
        form_data = {"first_name": "Mark", "last_name": "Bush", "username": "markbush", "email": "repeat@gmail.com",
                     "password1": "test12345", "password2": "no_match"}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_public_information_form(self):
        # Valid form - description, linkedin and links are not required
        form_data = {"city": "Lille", "description": None, "linkedin": None, "url_link_1": None, "url_link_2": None}
        form = PublicInformationForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Invalid form - city is required
        form_data = {"city": None, "description": None, "linkedin": None, "url_link_1": None, "url_link_2": None}
        form = PublicInformationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_private_information_form(self):
        # Valid form - the fields are not required
        form_data = {"gender": None, "phone_number": None, "dob": None}
        form = PrivateInformationForm(data=form_data)
        self.assertTrue(form.is_valid())

        # Invalid phone number
        form_data = {"gender": None, "phone_number": "123", "dob": "30/03/2010"}
        form = PrivateInformationForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Invalid dob 30Feb
        form_data = {"gender": None, "phone_number": None, "dob": "30/04/2010"}
        form = PrivateInformationForm(data=form_data)
        self.assertFalse(form.is_valid())
