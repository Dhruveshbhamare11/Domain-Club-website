from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("team/", views.team, name="team"),
    path("api/team/", views.team_api, name="team_api"),
    path("contact/", views.contact, name="contact"),
]
