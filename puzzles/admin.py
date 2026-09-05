from django.contrib import admin
from .models import Puzzle, Submission


@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "end_time", "is_processed", "winner", "created_at")
    readonly_fields = ("is_processed", "winner", "created_at")
    list_filter = ("is_processed",)
    search_fields = ("title",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("puzzle", "user", "submitted_value", "is_correct", "submitted_at")
    list_filter = ("is_correct",)
    search_fields = ("user__username", "puzzle__title")
