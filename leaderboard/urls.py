from django.urls import path
from . import views
app_name = "leaderboard"
urlpatterns = [path("", views.all_time, name="all_time"), path("monthly/", views.monthly, name="monthly")]
