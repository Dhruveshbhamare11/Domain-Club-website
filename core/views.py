from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ContactForm
from .models import TeamMember


def home(request):
    from puzzles.models import Puzzle
    from accounts.models import StudentProfile
    from events.models import Event
    from blog.models import BlogPost
    return render(request, "core/home.html", {
        "puzzle": Puzzle.objects.filter(start_time__lte=timezone.now(), end_time__gt=timezone.now()).first(),
        "leaders": StudentProfile.objects.select_related("user").order_by("cached_rank")[:5],
        "events": Event.objects.filter(date__gte=timezone.localdate())[:3],
        "posts": BlogPost.objects.filter(published=True)[:3], "team": TeamMember.objects.all()[:4],
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
