from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ContactForm
from .models import TeamMember


def home(request):
    puzzle = None
    leaders = []
    events = []
    posts = []
    team_members = []
    
    try:
        from puzzles.models import Puzzle
        now = timezone.now()
        puzzle = Puzzle.objects.filter(end_time__gt=now).order_by("-start_time").first()
        if not puzzle:
            puzzle = Puzzle.objects.order_by("-created_at").first()
    except Exception:
        pass

    try:
        from accounts.models import StudentProfile
        leaders = StudentProfile.objects.select_related("user").order_by(
            "-points", "-best_streak", "-current_streak", "cached_rank"
        )[:5]
    except Exception:
        pass

    try:
        from events.models import Event
        events = Event.objects.filter(date__gte=timezone.localdate())[:3]
    except Exception:
        pass

    try:
        from blog.models import BlogPost
        posts = BlogPost.objects.filter(published=True)[:3]
    except Exception:
        pass

    try:
        team_members = TeamMember.objects.all()[:4]
    except Exception:
        pass

    return render(request, "core/home.html", {
        "puzzle": puzzle,
        "leaders": leaders,
        "events": events,
        "posts": posts,
        "team": team_members,
    })


def about(request):
    return render(request, "core/about.html")


def team(request): return render(request, "core/team.html", {"team": TeamMember.objects.all()})


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        messages.success(request, "Thanks — we will get back to you soon.")
        return redirect("core:contact")
    return render(request, "core/contact.html", {"form": form})


def robots_txt(request):
    return HttpResponse("User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /login/\nDisallow: /register/\n", content_type="text/plain")
