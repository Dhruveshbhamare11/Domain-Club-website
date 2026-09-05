from django.shortcuts import get_object_or_404, render
from .models import Event
def event_list(request): return render(request, "events/events.html", {"events": Event.objects.all()})
def event_detail(request, slug): return render(request, "events/event_detail.html", {"event": get_object_or_404(Event, slug=slug)})
