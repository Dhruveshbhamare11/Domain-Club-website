from django.contrib.auth.models import User
from django.db import models


class Badge(models.Model):
    code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(max_length=100, blank=True)

    def __str__(self): return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="awards")
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "badge"), name="unique_user_badge")]
        ordering = ("-awarded_at",)
