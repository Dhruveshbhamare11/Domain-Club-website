from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from .models import Event

def event_list(request):
    events = cache.get("all_events_list")
    if events is None:
        events = list(Event.objects.all())
        cache.set("all_events_list", events, 120)
    return render(request, "events/events.html", {"events": events})

def event_detail(request, slug):
    return render(request, "events/event_detail.html", {"event": get_object_or_404(Event, slug=slug)})
