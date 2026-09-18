from django.db import models


class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    branch_year = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to="team/", blank=True)
    bio = models.TextField(blank=True)
    social_link = models.URLField(blank=True)
    anime_quote = models.CharField(max_length=255, blank=True, help_text="Famous anime dialogue or quote")
    anime_character = models.CharField(max_length=100, blank=True, help_text="Companion Anime Character (e.g., Luffy, Gojo, Zoro, Naruto)")
    special_power = models.CharField(max_length=150, blank=True, help_text="e.g., Domain Expansion: Infinite Logic")
    bounty_or_power = models.CharField(max_length=100, blank=True, help_text="e.g., Power Level: 9000+ or Bounty: ฿1,500,000,000")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("order", "name")
