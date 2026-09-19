from django.db.models import F
from accounts.models import StudentProfile
from .models import MonthlyScore, MonthlyWinner
from badges.services import award_badge


def update_monthly_score(submission):
    date = submission.puzzle.end_time
    score, _ = MonthlyScore.objects.get_or_create(user=submission.user, year=date.year, month=date.month)
    score.puzzles_participated += 1
    if submission.is_correct:
        score.points += 10
        score.correct_answers += 1
    score.best_streak = max(score.best_streak, submission.user.profile.current_streak)
    score.save()


def recalculate_ranks():
    profiles = list(StudentProfile.objects.select_related("user").order_by(
        "-points", "-best_streak", "-current_streak", "user__date_joined", "user__username"
    ))
    to_update = []
    for rank, profile in enumerate(profiles, 1):
        if profile.cached_rank != rank:
            profile.cached_rank = rank
            to_update.append(profile)
    if to_update:
        StudentProfile.objects.bulk_update(to_update, ["cached_rank"])
    return profiles


def record_monthly_winner(year, month):
    score = MonthlyScore.objects.filter(year=year, month=month).order_by("-points", "-correct_answers").first()
    if not score:
        return None
    winner, created = MonthlyWinner.objects.get_or_create(year=year, month=month, defaults={
        "user": score.user, "points": score.points, "correct_answers": score.correct_answers,
        "puzzles_participated": score.puzzles_participated, "best_streak": score.best_streak,
    })
    if created: award_badge(winner.user, "MONTHLY_WINNER")
    return winner
