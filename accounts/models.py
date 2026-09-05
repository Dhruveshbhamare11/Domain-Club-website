from django.contrib.auth.models import User
from django.db import models


class StudentProfile(models.Model):
    BRANCH_CHOICES = (
        ("COMPS", "COMPS"), ("IT", "IT"), ("EXTC", "EXTC"), ("MECH", "MECH"),
    )
    YEAR_CHOICES = (("FE", "FE"), ("SE", "SE"), ("TE", "TE"), ("BE", "BE"))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    #profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, default="profile_pics/default_avatar.png")
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    year = models.CharField(max_length=2, choices=YEAR_CHOICES)
    points = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    best_streak = models.PositiveIntegerField(default=0)
    cached_rank = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ("cached_rank", "user__username")

    def __str__(self):
        return self.user.get_full_name() or self.user.username
