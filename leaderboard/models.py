from django.contrib.auth.models import User
from django.db import models


class MonthlyScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="monthly_scores")
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    points = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    puzzles_participated = models.PositiveIntegerField(default=0)
    best_streak = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "year", "month"), name="unique_monthly_score")]
        indexes = [models.Index(fields=("year", "month", "-points"))]
        ordering = ("-points", "-best_streak", "-correct_answers", "user__username")


class MonthlyWinner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="monthly_wins")
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    points = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    puzzles_participated = models.PositiveIntegerField()
    best_streak = models.PositiveIntegerField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=("year", "month"), name="unique_monthly_winner")]
        ordering = ("-year", "-month")
