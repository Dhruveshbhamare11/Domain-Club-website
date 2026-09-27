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
    cache_key = f"event_detail_{slug}"
    event = cache.get(cache_key)
    if event is None:
        event = get_object_or_404(Event, slug=slug)
        cache.set(cache_key, event, 120)
    return render(request, "events/event_detail.html", {"event": event})
