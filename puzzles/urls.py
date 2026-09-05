from django.urls import path
from . import views
app_name = "puzzles"
urlpatterns = [path("", views.current_puzzle, name="current"), path("archive/", views.archive, name="archive"), path("<int:pk>/", views.puzzle_detail, name="detail"), path("<int:pk>/submit/", views.submit, name="submit")]
