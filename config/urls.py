from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.sitemaps import sitemaps
from core.views import robots_txt

from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls), path("", include("core.urls")),
    path("", include("accounts.urls")), path("puzzles/", include("puzzles.urls")),
    path("leaderboard/", include("leaderboard.urls")), path("badges/", include("badges.urls")),
    path("events/", include("events.urls")), path("blogs/", include("blog.urls")),
    path("blog/", RedirectView.as_view(url="/blogs/", permanent=True)),
    path("robots.txt", robots_txt, name="robots"), path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
