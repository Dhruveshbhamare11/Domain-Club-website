from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from events.models import Event
from blog.models import BlogPost
from puzzles.models import Puzzle


class StaticSitemap(Sitemap):
    def items(self): return ["core:home", "core:about", "core:team", "events:list", "blog:list", "puzzles:archive", "leaderboard:all_time"]
    def location(self, item): return reverse(item)


class EventSitemap(Sitemap):
    def items(self): return Event.objects.all()


class BlogSitemap(Sitemap):
    def items(self): return BlogPost.objects.filter(published=True)


class PuzzleSitemap(Sitemap):
    def items(self): return Puzzle.objects.all()
    def location(self, item): return reverse("puzzles:detail", args=(item.pk,))


sitemaps = {"static": StaticSitemap, "events": EventSitemap, "blogs": BlogSitemap, "puzzles": PuzzleSitemap}
