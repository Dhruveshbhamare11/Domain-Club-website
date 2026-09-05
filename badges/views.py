from django.shortcuts import render
from .models import Badge
def badge_list(request): return render(request, "badges/badges.html", {"badges": Badge.objects.all()})
