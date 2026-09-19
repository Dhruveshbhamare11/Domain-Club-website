from django.contrib import admin, messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Puzzle, Submission
from .services import process_puzzle, process_expired_puzzles


@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    change_list_template = "admin/puzzles/puzzle/change_list.html"
    list_display = (
        "title",
        "is_active_display",
        "start_time",
        "end_time",
        "is_processed_display",
        "process_button",
        "winner",
        "created_at",
    )
    readonly_fields = ("is_processed", "winner", "created_at")
    list_filter = ("is_processed",)
    search_fields = ("title",)
    actions = ["process_selected_puzzles", "process_all_expired_puzzles_action"]

    @admin.display(boolean=True, description="Active Now")
    def is_active_display(self, obj):
        return obj.is_active

    @admin.display(boolean=True, description="Is Processed")
    def is_processed_display(self, obj):
        return obj.is_processed

    @admin.display(description="Process Action")
    def process_button(self, obj):
        if obj.is_processed:
            return mark_safe(
                '<span style="background: #064e3b; color: #34d399; font-weight: 700; padding: 3px 8px; border-radius: 4px; font-size: 11px; border: 1px solid #059669; display: inline-block;">'
                '✓ PROCESSED'
                '</span>'
            )
        return format_html(
            '<a class="button" href="process/{}/" style="background: #2563eb; color: #ffffff !important; padding: 4px 10px; border-radius: 4px; font-weight: 700; font-size: 11px; text-decoration: none; display: inline-block; white-space: nowrap; box-shadow: 0 1px 3px rgba(0,0,0,0.3);">'
            '⚡ Process Puzzle'
            '</a>',
            obj.pk
        )

    def get_changeform_initial_data(self, request):
        from datetime import timedelta
        from django.utils import timezone
        now = timezone.now()
        return {
            "start_time": now,
            "end_time": now + timedelta(days=7),
        }

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("process/<int:puzzle_id>/", self.admin_site.admin_view(self.process_single_puzzle_view), name="puzzle_process_single"),
            path("process-all/", self.admin_site.admin_view(self.process_all_puzzles_view), name="puzzle_process_all"),
        ]
        return custom_urls + urls

    def process_single_puzzle_view(self, request, puzzle_id):
        puzzle = get_object_or_404(Puzzle, pk=puzzle_id)
        if puzzle.is_processed:
            self.message_user(request, f"Puzzle '{puzzle.title}' was already processed.", level=messages.INFO)
            return redirect("admin:puzzles_puzzle_changelist")

        result = process_puzzle(puzzle, force=True)
        if result:
            winner = result["winner"]
            winner_str = f"Winner: {winner.get_full_name() or winner.username}" if winner else "No correct solvers"
            self.message_user(
                request,
                f"Successfully processed '{puzzle.title}'! {winner_str}. Correct submissions: {result['correct']}, Points awarded: {result['points']}. Leaderboard updated!",
                level=messages.SUCCESS
            )
        else:
            self.message_user(request, f"Could not process '{puzzle.title}'.", level=messages.WARNING)
        return redirect("admin:puzzles_puzzle_changelist")

    def process_all_puzzles_view(self, request):
        results = process_expired_puzzles()
        if results:
            self.message_user(
                request,
                f"Successfully processed {len(results)} expired puzzle(s)! Leaderboard rankings, streaks, and badges have been updated.",
                level=messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                "No expired unprocessed puzzles were found. (To process an active puzzle right now, click its individual '⚡ Process Puzzle' button in the table).",
                level=messages.INFO
            )
        return redirect("admin:puzzles_puzzle_changelist")

    @admin.action(description="⚡ Process selected puzzles & update leaderboard")
    def process_selected_puzzles(self, request, queryset):
        processed_count = 0
        for puzzle in queryset:
            if not puzzle.is_processed:
                res = process_puzzle(puzzle, force=True)
                if res:
                    processed_count += 1
        self.message_user(
            request,
            f"Successfully processed {processed_count} puzzle(s). Leaderboard, streaks, and ranks updated!",
            level=messages.SUCCESS
        )

    @admin.action(description="🏆 Process all expired puzzles & update leaderboard")
    def process_all_expired_puzzles_action(self, request, queryset):
        results = process_expired_puzzles()
        self.message_user(
            request,
            f"Processed {len(results)} expired puzzle(s). Leaderboard updated!",
            level=messages.SUCCESS
        )


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("puzzle", "user", "submitted_value", "is_correct", "submitted_at")
    list_filter = ("is_correct",)
    search_fields = ("user__username", "puzzle__title")
