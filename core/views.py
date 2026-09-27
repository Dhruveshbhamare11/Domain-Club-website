from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from django.core.cache import cache
from .forms import ContactForm
from .models import TeamMember


def home(request):
    data = cache.get("home_page_data")
    if data is None:
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
            leaders = list(StudentProfile.objects.select_related("user").order_by(
                "-points", "-best_streak", "-current_streak", "cached_rank"
            )[:5])
        except Exception:
            pass

        try:
            from events.models import Event
            events = list(Event.objects.filter(date__gte=timezone.localdate())[:3])
        except Exception:
            pass

        try:
            from blog.models import BlogPost
            posts = list(BlogPost.objects.filter(published=True)[:3])
        except Exception:
            pass

        try:
            team_members = list(TeamMember.objects.all()[:4])
        except Exception:
            pass

        data = {
            "puzzle": puzzle,
            "leaders": leaders,
            "events": events,
            "posts": posts,
            "team": team_members,
        }
        cache.set("home_page_data", data, 60)

    return render(request, "core/home.html", data)


def about(request):
    return render(request, "core/about.html")


from django.views.decorators.cache import cache_control
from django.http import HttpResponse, JsonResponse


@cache_control(no_cache=True, must_revalidate=True)
def team(request):
    team_members = cache.get("team_all_members")
    if team_members is None:
        team_members = list(TeamMember.objects.all())
        cache.set("team_all_members", team_members, 120)
    return render(request, "core/team.html", {"team": team_members})


def team_api(request):
    """
    Public JSON API for team members.
    Enables external or standalone frontends (like GDGC Minecraft homepage)
    to dynamically fetch and render team members managed via Django Admin.
    """
    team_members = cache.get("team_all_members")
    if team_members is None:
        team_members = list(TeamMember.objects.all())
        cache.set("team_all_members", team_members, 120)

    data = [
        {
            "id": m.id,
            "name": m.name,
            "role": m.role,
            "branch_year": m.branch_year,
            "avatar": m.avatar,
            "bio": m.bio,
            "social_link": m.social_link,
            "anime_character": m.anime_character,
            "anime_quote": m.anime_quote,
            "special_power": m.special_power,
            "bounty_or_power": m.bounty_or_power,
            "order": m.order,
        }
        for m in team_members
    ]
    response = JsonResponse({"team": data}, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    return response


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        messages.success(request, "Thanks — we will get back to you soon.")
        return redirect("core:contact")
    return render(request, "core/contact.html", {"form": form})


def robots_txt(request):
    return HttpResponse("User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /login/\nDisallow: /register/\n", content_type="text/plain")
