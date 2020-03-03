from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from .models import Area

# Test all pages functional for logged-in users
class LoggedIn(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser',is_active=True,email="test@test.com")
        user.set_password('12345')
        user.save()

        self.client = Client()
        self.client.login(username='testuser', password='12345')

        # Add the following pre-defined categories:
        area_names = ["Video & Animation", "Graphics & Design", "Writing", "Translation", "Technology", "Music & Audio"]
        for name in area_names:
            if not Area.objects.filter(name=name).exists():
                area = Area(name=name)
                area.save()

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
