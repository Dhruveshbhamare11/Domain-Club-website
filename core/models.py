from django.db import models


class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    branch_year = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to="team/", blank=True)
    bio = models.TextField(blank=True)
    social_link = models.URLField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta: ordering = ("order", "name")
