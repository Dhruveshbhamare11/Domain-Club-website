from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    def test_registration_creates_profile_and_logs_student_in(self):
        response = self.client.post(reverse("accounts:register"), {
            "first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.test",
            "branch": "COMPS", "year": "SE",
            "password1": "strong-test-password-123", "password2": "strong-test-password-123",
        })
        self.assertRedirects(response, reverse("core:home"))
        self.assertEqual(response.wsgi_request.user.email, "ada@example.test")
        self.assertEqual(response.wsgi_request.user.profile.branch, "COMPS")

    def test_student_can_log_in_using_email(self):
        self.client.post(reverse("accounts:register"), {
            "first_name": "Ada", "last_name": "Lovelace", "email": "ada@example.test",
            "branch": "COMPS", "year": "SE", "password1": "secret1", "password2": "secret1",
        })
        self.client.logout()
        response = self.client.post(reverse("accounts:login"), {"username": "ada@example.test", "password": "secret1"})
        self.assertRedirects(response, reverse("core:home"))

    def test_invalid_login_stays_on_login_page(self):
        response = self.client.post(reverse("accounts:login"), {"username": "none", "password": "wrong"})
        self.assertEqual(response.status_code, 200)
