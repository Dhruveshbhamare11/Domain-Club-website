from decimal import Decimal

from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from accounts.models import StudentProfile
from badges.services import award_badge, award_streak_badges
from leaderboard.services import recalculate_ranks, record_monthly_winner, update_monthly_score

from .models import Puzzle, Submission


def answers_match(value, answer):
    return Decimal(value) == Decimal(answer)


@transaction.atomic
def process_puzzle(puzzle):
    puzzle = Puzzle.objects.select_for_update().get(pk=puzzle.pk)
    if puzzle.is_processed or timezone.now() < puzzle.end_time:
        return None
    submissions = {item.user_id: item for item in Submission.objects.filter(puzzle=puzzle).select_related("user", "user__profile")}
    winner_submission = Submission.objects.filter(puzzle=puzzle, is_correct=True).select_related("user").order_by("submitted_at").first()
    if winner_submission:
        puzzle.winner = winner_submission.user
        award_badge(winner_submission.user, "FIRST_WIN")

    points_awarded = 0
    for profile in StudentProfile.objects.select_for_update().select_related("user"):
        submission = submissions.get(profile.user_id)
        if submission and submission.is_correct:
            profile.points += 10
            profile.current_streak += 1
            profile.best_streak = max(profile.best_streak, profile.current_streak)
            points_awarded += 10
            profile.save(update_fields=("points", "current_streak", "best_streak"))
            award_streak_badges(profile.user)
        else:
            if profile.current_streak:
                profile.current_streak = 0
                profile.save(update_fields=("current_streak",))
        if submission:
            update_monthly_score(submission)

    puzzle.is_processed = True
    puzzle.save(update_fields=("winner", "is_processed"))
    award_perfect_month_badges(puzzle)
    recalculate_ranks()
    return {"puzzle": puzzle, "winner": puzzle.winner, "correct": sum(s.is_correct for s in submissions.values()), "points": points_awarded}


def award_perfect_month_badges(puzzle):
    """Award a completed calendar month's flawless participants exactly once."""
    local_end = timezone.localtime(puzzle.end_time)
    monthly_puzzles = Puzzle.objects.filter(
        end_time__year=local_end.year, end_time__month=local_end.month, is_processed=True
    )
    puzzle_count = monthly_puzzles.count()
    if not puzzle_count:
        return
    for profile in StudentProfile.objects.select_related("user"):
        correct_count = Submission.objects.filter(
            user=profile.user, puzzle__in=monthly_puzzles, is_correct=True
        ).count()
        if correct_count == puzzle_count:
            award_badge(profile.user, "PERFECT_MONTH")


def process_expired_puzzles():
    results = []
    for puzzle in Puzzle.objects.filter(end_time__lte=timezone.now(), is_processed=False):
        result = process_puzzle(puzzle)
        if result: results.append(result)
    now = timezone.localtime()
    months = Puzzle.objects.filter(end_time__lt=now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)).dates("end_time", "month")
    for date in months:
        record_monthly_winner(date.year, date.month)
    return results
