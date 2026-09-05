from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    title = models.CharField(max_length=240)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=300)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="blog/", blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    class Meta:
        ordering = ("-published_at", "-created_at")
        indexes = [models.Index(fields=("published", "published_at"))]
    def __str__(self): return self.title
    def get_absolute_url(self): return reverse("blog:detail", args=(self.slug,))
