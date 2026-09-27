from django.test import TestCase
from django.urls import reverse


class SeoTests(TestCase):
    def test_robots_and_sitemap_are_public(self):
        self.assertContains(self.client.get(reverse("robots")), "Disallow: /admin/")
        self.assertEqual(self.client.get(reverse("sitemap")).status_code, 200)

    def test_home_has_metadata(self):
        self.assertContains(self.client.get(reverse("core:home")), "description")

    def test_team_page_and_api(self):
        from core.models import TeamMember
        member = TeamMember.objects.create(name="Unit Test Member", role="Tester", order=100)
        
        # Test team page status
        response = self.client.get(reverse("core:team"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unit Test Member")
        
        # Test team API
        api_response = self.client.get(reverse("core:team_api"))
        self.assertEqual(api_response.status_code, 200)
        self.assertContains(api_response, "Unit Test Member")

