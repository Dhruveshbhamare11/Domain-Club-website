from django.core.cache import cache
from django.utils import timezone
from django.shortcuts import render
from accounts.models import StudentProfile
from .models import MonthlyScore, MonthlyWinner
from .services import recalculate_ranks


def all_time(request):
    profiles = cache.get("all_time_profiles_data")
    if profiles is None:
        profiles = list(StudentProfile.objects.select_related("user").order_by(
            "-points", "-best_streak", "-current_streak", "cached_rank", "user__username"
        ))
        cache.set("all_time_profiles_data", profiles, 60)
    return render(request, "leaderboard/all_time.html", {"profiles": profiles})


def monthly(request):
    now = timezone.localtime()
    year = int(request.GET.get("year", now.year))
    month = int(request.GET.get("month", now.month))
    cache_key = f"monthly_scores_{year}_{month}"
    cached_data = cache.get(cache_key)
    if cached_data is None:
        scores = list(MonthlyScore.objects.filter(year=year, month=month).select_related("user", "user__profile"))
        winners = list(MonthlyWinner.objects.all())
        cached_data = {"scores": scores, "winners": winners}
        cache.set(cache_key, cached_data, 60)
    return render(request, "leaderboard/monthly.html", {
        "scores": cached_data["scores"],
        "year": year,
        "month": month,
        "winners": cached_data["winners"]
    })
