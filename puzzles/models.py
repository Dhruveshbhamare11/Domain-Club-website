from datetime import timedelta
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Puzzle(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    correct_answer = models.CharField(max_length=100)
    solution = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="puzzle_wins")
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-start_time",)
        indexes = [models.Index(fields=("start_time", "end_time", "is_processed"))]

    def clean(self):
        try:
            Decimal(self.correct_answer)
        except (InvalidOperation, TypeError):
            raise ValidationError({"correct_answer": "Enter a valid integer or decimal."})

    # def save(self, *args, **kwargs):
    #     """Guarantee production puzzles last 24 hours; allow local short-window tests."""
    #     if self.end_time is None or not settings.DEBUG:
    #         self.end_time = self.start_time + timedelta(hours=24)
    #     self.full_clean()
    #     super().save(*args, **kwargs)

    @property
    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_time <= now < self.end_time

    @property
    def is_closed(self):
        from django.utils import timezone
        return timezone.now() >= self.end_time

    def __str__(self): return self.title


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name="submissions")
    submitted_value = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "puzzle"), name="unique_submission_per_puzzle")]
        indexes = [models.Index(fields=("puzzle", "is_correct", "submitted_at"))]
        ordering = ("submitted_at",)
