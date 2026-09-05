from django.db import models
from django.urls import reverse


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to="events/", blank=True)
    registration_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ("date", "time")
        indexes = [models.Index(fields=("date",))]
    def __str__(self): return self.title
    def get_absolute_url(self): return reverse("events:detail", args=(self.slug,))
