from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "branch", "year", "points", "current_streak", "best_streak", "cached_rank")
    list_select_related = ("user",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "branch")
    list_filter = ("year", "branch")
