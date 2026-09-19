from django.contrib import admin
from .models import Puzzle, Submission


@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active_display", "start_time", "end_time", "is_processed", "winner", "created_at")
    readonly_fields = ("is_processed", "winner", "created_at")
    list_filter = ("is_processed",)
    search_fields = ("title",)

    @admin.display(boolean=True, description="Active Now")
    def is_active_display(self, obj):
        return obj.is_active

    def get_changeform_initial_data(self, request):
        from datetime import timedelta
        from django.utils import timezone
        now = timezone.now()
        return {
            "start_time": now,
            "end_time": now + timedelta(days=7),
        }


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("puzzle", "user", "submitted_value", "is_correct", "submitted_at")
    list_filter = ("is_correct",)
    search_fields = ("user__username", "puzzle__title")
