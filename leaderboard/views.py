from django.utils import timezone
from django.shortcuts import render
from accounts.models import StudentProfile
from .models import MonthlyScore, MonthlyWinner


def all_time(request):
    return render(request, "leaderboard/all_time.html", {"profiles": StudentProfile.objects.select_related("user").order_by("cached_rank", "user__username")})


def monthly(request):
    now = timezone.localtime()
    year = int(request.GET.get("year", now.year)); month = int(request.GET.get("month", now.month))
    scores = MonthlyScore.objects.filter(year=year, month=month).select_related("user", "user__profile")
    return render(request, "leaderboard/monthly.html", {"scores": scores, "year": year, "month": month, "winners": MonthlyWinner.objects.all()})
