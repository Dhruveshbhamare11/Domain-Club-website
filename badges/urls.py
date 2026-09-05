from django.urls import path
from .views import badge_list
app_name = "badges"
urlpatterns = [path("", badge_list, name="list")]
