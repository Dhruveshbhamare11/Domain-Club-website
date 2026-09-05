from django.test import TestCase
from django.urls import reverse


class SeoTests(TestCase):
    def test_robots_and_sitemap_are_public(self):
        self.assertContains(self.client.get(reverse("robots")), "Disallow: /admin/")
        self.assertEqual(self.client.get(reverse("sitemap")).status_code, 200)

    def test_home_has_metadata(self):
        self.assertContains(self.client.get(reverse("core:home")), "description")
